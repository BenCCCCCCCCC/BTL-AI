using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json.Linq;

namespace BTL
{
    // A read-only projection of the current run. Presentation never settles an action.
    public sealed class ChapterPresentation
    {
        readonly ChapterSession session;
        public JObject Data { get; }
        public ChapterPresentation(ChapterSession session, string json)
        { this.session = session; Data = JObject.Parse(json); }
        static string S(JToken t) => ChapterSession.S(t);
        public string SourceNode => session.Node == "result" ?
            S(session.History.LastOrDefault(h => S(h["action"]) != "settle")?["node"]) : session.Node;
        public string Actor => new[] {"N10","N40"}.Contains(SourceNode) ? "witness" :
            new[] {"N50","N51","N60"}.Contains(SourceNode) ? "clerk" : "editor";
        public string Scene => new[] {"N10","N30","N40"}.Contains(SourceNode) ? "yard" :
            new[] {"N50","N51","N60"}.Contains(SourceNode) ? "records" : "desk";
        public string Stage => session.Finished ? "归档" : session.Node == "N90" || session.Node == "aftermath" ||
            new[] {"N91","N92","N93","N94","N95","N96"}.Contains(session.Node) ? "余波" :
            new[] {"N70","N80","N81","N82"}.Contains(session.Node) ? "写作" : "调查";
        public string EndingTitle => S(Data["endings"]?[session.Ending ?? ""]?["title"]);
        public string EndingText => S(Data["endings"]?[session.Ending ?? ""]?["text"]);
        public string Display(string text) => (text ?? "").Replace("Company A", "澄川实业");
        public string Tradeoff(string scene)
        {
            if (session.Slots != 1) return "";
            var others = session.AvailableScenes().Where(s => s != scene)
                .Select(s => S(Data["investigations"]?[s]?["title"])).ToArray();
            return others.Length > 0 ? "这是最后一段。选择这里，本局就来不及：" + string.Join("、", others) + "。" :
                "这是最后一段。也可以保留现有材料，直接回到编辑台。";
        }
        public IEnumerable<(string actor, string text)> Aftermath()
        {
            yield return ("editor", S(Data["aftermath"]?["editor"]?[session.Ending ?? ""]));
            // Reuse the actual authored responses instead of making a second outcome rule engine.
            // These scenes add staging only when the canonical response really happened.
            foreach (string key in new[] { "witness_closed", "witness_omitted", "witness_clarified", "witness_kept", "witness_open",
                "clerk_closed_with_ledger", "clerk_closed_no_ledger", "uses_published", "uses_known", "uses_unknown" })
            {
                string original = S(session.Data["copy"]?[key]);
                if (original.Length == 0 || !session.PeopleText.Contains(original)) continue;
                string actor = key.StartsWith("witness_") ? "witness" : "clerk";
                string scene = key.StartsWith("witness_") ? key.Substring(8) : key.StartsWith("clerk_") ? key.Substring(6) : key;
                yield return (actor, S(Data["aftermath"]?[actor]?[scene]));
            }
        }
        public string Note(string id)
        {
            if (id == ChapterSession.Video && !session.Evidence.ContainsKey(ChapterSession.Audio))
                return S(Data["notes"]["video_without_audio"]) + (session.Evidence.ContainsKey(ChapterSession.Ledger) ?
                    "可以回看已有记录，再决定怎样写。" : "我还没有核查付款记录。");
            return S(Data["notes"]?[id]);
        }
        public string LatestEvidence
        {
            get
            {
                var h = session.History.LastOrDefault(x => S(x["action"]) != "settle");
                if (S(h?["action"]) == "save_video") return ChapterSession.Video;
                return S(h?["evidence"]);
            }
        }
        public IEnumerable<string> OpenQuestions()
        {
            if (!session.Evidence.ContainsKey(ChapterSession.Video)) yield return "现场顺序 · 本局尚未完成核查";
            if (!session.Evidence.ContainsKey(ChapterSession.Ledger)) yield return "行动付款 · 本局尚未取得账页";
            if (session.Evidence.ContainsKey(ChapterSession.Audio) && session.Evidence.ContainsKey(ChapterSession.Video) &&
                !session.Evidence.ContainsKey(ChapterSession.Clarification))
                yield return "目击者观察范围 · " + (session.Cooperates("witness") ? "本局未完成回访" : "阿岑已结束后续合作");
            if (session.Evidence.ContainsKey(ChapterSession.Ledger) && !session.Evidence.ContainsKey(ChapterSession.Context))
                yield return "账目科目与范围 · " + (session.Cooperates("clerk") ? "本局未完成回访" : "许先生已结束后续合作");
        }
        public IEnumerable<(string title,string body)> Recap()
        {
            foreach (var h in session.History)
            {
                string node = S(h["node"]), action = S(h["action"]), original = S(h["text"]);
                var script = (session.Data["scripts"]?[node] as JArray)?.FirstOrDefault(s => S(s["id"]) == action);
                if (script != null)
                {
                    string body = "你：" + original + "\n\n" + S(h["response"]);
                    string evidence = S(h["evidence"]);
                    if (session.Evidence.TryGetValue(evidence, out var e)) body += "\n\n留存：" + S(e["title"]);
                    yield return (S(script["label"]), body);
                }
                else if (action == "save_video") yield return ("保存现场影像", "你留存了主通道连续画面，供选稿时核对。");
                else if (action == "settle") yield return ("结束一场调查", S(Data["investigations"]?[S(h["scene"])]?["title"]) + " · 使用一段时间。");
                else if (action == "leave") yield return ("结束访问", node == "N10" ? "你没有采用初访，也没有取得录音。" : "你结束了这次访问，没有取得新的材料。");
                else if (action == "cancel_pending") yield return ("取消待确认报价", "回到交涉，尚未支付费用。");
                else if (action == "publish") yield return ("签发这一版", S(session.Publication?["headline"]) +
                    "\n\n" + EndingTitle + "\n\n" + session.OutcomeText + "\n\n" + session.PeopleText);
                else if (action == "hold") yield return ("决定暂缓", "本版没有刊发，没有生成刊发快照。\n\n" + session.OutcomeText);
            }
        }
        public IEnumerable<string> WorkSheet()
        {
            if (session.Ending == "N94") yield return "编辑要求的复核与跟进\n" + session.OutcomeText;
            if (session.Ending == "N92") yield return session.Evidence.ContainsKey(ChapterSession.Video) ?
                "后续工作：说明录音与画面之间的冲突。" : "后续工作：核查现场顺序。";
            if (session.Publication?["claims"] is JArray claims && session.Publication?["evaluations"] is JArray evaluations)
            {
                for (int i=0;i<claims.Count;i++)
                {
                    string state = S(evaluations[i]["underlying"]);
                    yield return ChapterSession.DescribeClaim((JObject)claims[i]) + "\n" +
                        (state == "SUPPORTED" ? "本局留存了相应记录。" : state == "CONTRADICTED" ?
                         "现有记录中有不同方向的内容，须保留并解释。" : "本局尚未取得可说明这一事实的记录。") +
                        (S(claims[i]["source_ref_id"]).Length > 0 ? "来源原话与事实经过分别归档。" : "");
                }
            }
            if (session.Events.Any(e => S(e["id"]) == "ledger_purchase")) yield return "取证经过：支付 500 取得副本；付款经过与材料一起留档。";
            if (session.Events.Any(e => S(e["id"]).StartsWith("pressure_"))) yield return "采访经过：本局发生过身份施压；刊发结果不撤销已经结束的来源合作。";
        }
    }
}
