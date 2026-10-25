using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json.Linq;

namespace BTL
{
    public sealed class ChapterInterview
    {
        readonly ChapterSession session;
        JObject candidate;
        string choiceId, original;
        int revision;
        string node;
        public string Draft { get; private set; } = "";
        public string Message { get; private set; } = "";
        public bool HasReview => choiceId != null;
        public ChapterInterview(ChapterSession session) { this.session = session; }
        public void Edit(string text = null)
        {
            if (text != null) Draft = text;
            candidate = null; choiceId = null; original = null; Message = "";
        }
        bool Active => !session.Finished && session.Data["scripts"]?[session.Node] != null;
        public bool Prepare(string text)
        {
            Edit(text);
            if (!Active) throw new InvalidOperationException("Interview unavailable");
            if (string.IsNullOrWhiteSpace(text))
            { Message = "先写一句你想说的话，或载入一条离线示例。"; return false; }
            var script = session.AvailableScripts().FirstOrDefault(s => ChapterSession.S(s["text"]) == text.Trim());
            if (script == null)
            { Message = "原句已保留。这段文字不在离线脚本中，当前没有系统理解可供确认。"; return false; }
            var proposed = (JObject)script["candidate"];
            if (ChapterSession.S(proposed["status"]) == "AMBIGUOUS")
            { Message = "还不能确定“那个”指什么。原句已保留，请返回改写。"; return false; }
            if (!session.DialogueValid(proposed))
            { Message = "这次没有可执行的系统理解。原句已保留，采访尚未发生。"; return false; }
            candidate = (JObject)proposed.DeepClone(); choiceId = ChapterSession.S(script["id"]);
            original = text; revision = session.Revision; node = session.Node;
            return true;
        }
        public void PrepareLeave()
        {
            if (!Active || !session.Choices().Any(x => x.id == "leave")) throw new InvalidOperationException("Leaving unavailable");
            candidate = null; choiceId = "leave"; original = Draft; revision = session.Revision; node = session.Node;
            Message = "";
        }
        public IReadOnlyList<string> ReviewLines()
        {
            if (!HasReview) return Array.Empty<string>();
            if (choiceId == "leave") return new[] { "不发送保留的草稿。", node == "N10" ?
                "不采用初访，不取得录音。" : "结束本次访问，用一段调查时间，不取得新材料。" };
            string act = ChapterSession.S(candidate["act"]), target = ChapterSession.S(candidate["target_id"]);
            string action = act == "ACCEPT" ? "接受当前唯一交易，支付500并取得副本" :
                act == "REFUSE" ? "拒绝当前交易并结束本次访问" :
                target == ChapterSession.Fire ? "询问本次冲突谁先开火" :
                target == ChapterSession.Funding ? "询问本次行动谁付款" :
                target == ChapterSession.View ? "核对目击者首枪时的位置与可见范围" :
                target == ChapterSession.Uses ? "询问 R17 科目代码的具体名称" :
                target == "PROP_R17_RECORDS_FIRE_ORDER" ? "核对这份账是否能说明开火命令" :
                target == "REQ_HAND_OVER_LEDGER" ? "请求交付付款账页副本" :
                "提出支付500换账页副本；还未成交";
            var lines = new List<string> { "我准备做的事：" + action };
            string[] tactics = ((JArray)candidate["tactics"]).Select(ChapterSession.S).ToArray();
            foreach (string t in tactics) lines.Add(t == "THREAT" ? "施压：以公开名字作为不配合的后果。" :
                t == "ACCUSATION" ? "指控：指责对方在误导你。" : "旁敲侧击：暗示对方隐瞒，试图引出回答。");
            if (tactics.Length == 0) lines.Add("说话方式：没有附加施压、指控或旁敲侧击。");
            foreach (JToken e in (JArray)candidate["evidence_ref_ids"])
                lines.Add("提及材料：" + ChapterSession.S(session.Evidence[ChapterSession.S(e)]["title"]));
            if (((JArray)candidate["evidence_ref_ids"]).Count == 0) lines.Add("提及材料：没有引用已知证据。");
            lines.Add("确认才执行此项行动；不会承诺替来源刊发或保证其说法真实。");
            return lines;
        }
        public string ReviewedOriginal => original;
        public string Confirm()
        {
            if (!HasReview || !Active) throw new InvalidOperationException("No current interview review");
            if (node != session.Node || revision != session.Revision ||
                (choiceId != "leave" && (!session.DialogueValid(candidate) ||
                 !session.AvailableScripts().Any(s => ChapterSession.S(s["id"]) == choiceId &&
                     ChapterSession.S(s["text"]) == original.Trim() && JToken.DeepEquals(s["candidate"], candidate)))))
            {
                Edit(); Message = "采访条件已经变化。原句已保留，请重新复核。";
                throw new InvalidOperationException("Review stale");
            }
            string response;
            if (choiceId == "leave") { session.Choose("leave"); response = session.ResultText; }
            else response = session.ExecuteScript(choiceId, candidate, original);
            Edit(); return response;
        }
    }
}
