using System;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace BTL
{
    // The chapter JSON is authored content. Only this session may change canonical game state.
    public sealed class ChapterSession
    {
        public const string Audio = "EV_AUDIO_A", Video = "EV_VIDEO_A", Ledger = "EV_LEDGER_A";
        public const string Clarification = "EV_WITNESS_CLARIFICATION_A", Context = "EV_LEDGER_CONTEXT_A";
        public const string Fire = "PROP_FIRE_FIRST", Funding = "PROP_FUNDED_OPERATION";
        public const string View = "PROP_WITNESS_FIRST_SHOT_VIEW", Uses = "PROP_R17_RECORDED_USES";
        static readonly Dictionary<string, string> SceneNodes = new Dictionary<string, string>
        { {"A","N30"}, {"B","N50"}, {"S-A","N40"}, {"S-B","N60"} };
        static readonly Dictionary<string, string> SceneLabels = new Dictionary<string, string>
        { {"A","核查现场影像"}, {"B","核对付款账页"}, {"S-A","核对目击者观察范围"}, {"S-B","核对账目记录语境"} };

        readonly JObject data;
        readonly HashSet<string> visited = new HashSet<string>();
        readonly Dictionary<string, JObject> evidence = new Dictionary<string, JObject>();
        readonly HashSet<string> sources = new HashSet<string>();
        readonly Dictionary<string, bool> cooperation = new Dictionary<string, bool> { {"witness",true}, {"clerk",true} };
        readonly List<JObject> history = new List<JObject>();
        readonly List<JObject> events = new List<JObject>();
        JArray reviewedClaims;
        string reviewedText, reviewedBasis;
        int reviewHistoryCount;
        string activeScene, entryScene, pending;

        public string Node { get; private set; } = "N00";
        public int Revision { get; private set; }
        public int Slots { get; private set; }
        public int Money { get; private set; }
        public int Reputation { get; private set; }
        public int ThreatLevel { get; private set; }
        public int PublicOpinion { get; private set; }
        public string Draft { get; private set; } = "";
        public string HeadlineMessage { get; private set; } = "";
        public string ResultText { get; private set; } = "";
        public string Ending { get; private set; }
        public string OutcomeText { get; private set; } = "";
        public string PeopleText { get; private set; } = "";
        JObject publication;
        public JObject Publication => publication == null ? null : (JObject)publication.DeepClone();
        public bool Finished => Node == "N99";
        public IReadOnlyDictionary<string, JObject> Evidence => evidence;
        public IReadOnlyList<JObject> Events => events;
        public JObject Data => data;
        public JArray History => new JArray(history.Select(h => h.DeepClone()));
        public bool Cooperates(string role) => cooperation.TryGetValue(role, out var open) && open;
        public bool Visited(string scene) => visited.Contains(scene);

        public ChapterSession(string json)
        {
            data = JObject.Parse(json);
            if (!new[] { "RAILYARD_CHAPTER_1.0", "RAILYARD_CHAPTER_1.1" }.Contains(S(data["version"])))
                throw new ArgumentException("Wrong chapter version");
            Slots = I(data["investigation_slots"]); Money = I(data["initial_money"]);
        }
        public static string S(JToken token) => token == null ? "" : token.Value<string>() ?? "";
        static int I(JToken token) => token == null ? 0 : token.Value<int>();
        static bool B(JToken token) => token != null && token.Value<bool>();
        static JArray Arr(JToken token) => token as JArray ?? new JArray();
        static bool Has(JToken array, string value) => Arr(array).Any(x => S(x) == value);
        void Record(string action, string text = "")
        { Revision++; history.Add(new JObject { ["node"] = Node, ["action"] = action, ["text"] = text }); }
        void Event(string id)
        {
            if (events.Any(x => S(x["id"]) == id)) return;
            var authored = (JObject)data["events"][id];
            string resultId = S(data["version"]) + ":" + Revision + ":" + id;
            var effects = (JObject)authored["effects"];
            Money += I(effects["Money"]); Reputation += I(effects["Reputation"]);
            ThreatLevel += I(effects["Threat Level"]); PublicOpinion += I(effects["Public Opinion"]);
            events.Add(new JObject { ["id"] = id, ["label"] = S(authored["label"]),
                ["effects"] = effects.DeepClone(), ["result_id"] = resultId });
        }
        public IReadOnlyList<string> AvailableScenes()
        {
            if (Node != "N20" || Slots < 1) return Array.Empty<string>();
            return SceneNodes.Keys.Where(s => !visited.Contains(s) &&
                (s != "S-A" || evidence.ContainsKey(Audio) && evidence.ContainsKey(Video) && cooperation["witness"]) &&
                (s != "S-B" || evidence.ContainsKey(Ledger) && cooperation["clerk"])).ToArray();
        }
        public IReadOnlyList<JObject> AvailableScripts()
        {
            return Arr(data["scripts"]?[Node]).Cast<JObject>()
                .Where(x => S(x["id"]) != "accept" || Money >= 500).ToArray();
        }
        public IReadOnlyDictionary<string, JObject> VisibleHeadlines()
        {
            return ((JObject)data["headlines"]).Properties().Where(p => !B(p.Value["boundary_only"]) &&
                Arr(p.Value["requires_evidence"]).All(e => evidence.ContainsKey(S(e))))
                .ToDictionary(p => p.Name, p => (JObject)p.Value);
        }
        void Grant(string id, string variant = "")
        {
            var material = (JObject)data["evidence"]?[id]?.DeepClone();
            if (material == null) throw new InvalidOperationException("Unknown evidence: " + id);
            string selected = S(material["variants"]?[variant]);
            if (selected.Length > 0) material["text"] = selected;
            material.Remove("variants"); evidence[id] = material;
            if (id == Audio) sources.Add("SRC_WITNESS_A");
        }
        void Settle()
        {
            if (activeScene != null)
            {
                if (visited.Contains(activeScene) || Slots < 1) throw new InvalidOperationException("Scene already settled");
                visited.Add(activeScene); Slots--;
                history.Add(new JObject { ["node"] = Node, ["action"] = "settle", ["scene"] = activeScene, ["cost"] = 1 });
                activeScene = null;
            }
            pending = null;
        }
        void Result(string text) { ResultText = text; Node = "result"; }

        public bool DialogueValid(JObject candidate)
        {
            if (S(candidate?["status"]) != "RESOLVED") return false;
            string act = S(candidate["act"]), target = S(candidate["target_id"]);
            if (act == "ACCEPT" || act == "REFUSE")
                return Node == "N51" && pending == "PENDING_LEDGER_500" &&
                    (act == "REFUSE" || Money >= 500) && target.Length == 0 &&
                    candidate["value_id"] == null && candidate["polarity"] == null &&
                    Arr(candidate["evidence_ref_ids"]).All(x => evidence.ContainsKey(S(x)));
            var definition = data["targets"]?[target];
            if (definition == null || !Has(definition["dialogue_nodes"], Node) || !Has(definition["acts"], act)) return false;
            if (act == "REQUEST" && S(definition["kind"]) != "REQUEST") return false;
            if (act == "OFFER" && S(definition["kind"]) != "DEAL") return false;
            if (candidate["value_id"] != null && !Has(definition["values"], S(candidate["value_id"]))) return false;
            if (candidate["polarity"] != null) return false;
            if (act == "OFFER" && Arr(candidate["tactics"]).Count > 0) return false;
            if (Arr(candidate["tactics"]).Any(x => !new[] {"THREAT","ACCUSATION","INDIRECT_PROBE"}.Contains(S(x)))) return false;
            return Arr(candidate["evidence_ref_ids"]).All(x => evidence.ContainsKey(S(x)));
        }
        public string ExecuteScript(string id, JObject candidate, string original = null)
        {
            var script = AvailableScripts().FirstOrDefault(x => S(x["id"]) == id);
            if (script == null || !JToken.DeepEquals(script["candidate"], candidate) || !DialogueValid(candidate))
                throw new InvalidOperationException("Script unavailable or candidate changed");
            Record(id, original ?? S(script["text"]));
            var transcript = history.Last();
            string response = S(script["response"]);
            if (S(script["event"]).Length > 0) Event(S(script["event"]));
            if (S(script["grant"]).Length > 0) Grant(S(script["grant"]), S(script["variant"]));
            if (S(script["pressure"]).Length > 0)
            {
                string role = S(script["pressure"]); cooperation[role] = false; Event("pressure_" + role);
                response += "\n\n" + S(data["copy"]?["pressure_record"]);
            }
            if (B(script["finish"])) { Settle(); Result(response); }
            else if (S(script["next"]).Length > 0)
            { pending = "PENDING_LEDGER_500"; ResultText = response; Node = S(script["next"]); }
            else ResultText = response;
            transcript["response"] = response;
            if (S(script["grant"]).Length > 0) transcript["evidence"] = S(script["grant"]);
            return response;
        }
        public string Background(string label)
        {
            var text = data["nodes"]?[Node]?["background"]?[label];
            if (text == null) throw new InvalidOperationException("Background unavailable");
            Record("background", label); ResultText = S(text); return ResultText;
        }
        public IReadOnlyList<(string id, string label)> Choices()
        {
            var c = new List<(string,string)>();
            if (Node == "N00") c.Add(("begin","去见目击者"));
            if (Node == "N20")
            { c.AddRange(AvailableScenes().Select(s => ("visit:" + s, SceneLabels[s] + " · 一段"))); c.Add(("desk","结束调查，回编辑台")); }
            if (Node == "entry") { c.Add(("cancel_entry","返回安排 · 尚未进场")); c.Add(("enter","确认进入 · 本场结束用一段")); }
            if (Node == "desk_confirm") { c.Add(("cancel_desk","返回调查安排")); c.Add(("finish_investigation","确认结束调查")); }
            if (Node == "N30") { c.Add(("save_video","调出并保存这段记录")); c.Add(("leave","结束现场核查 · 用一段，不取记录")); }
            if (new[] {"N10","N40","N50","N60"}.Contains(Node)) c.Add(("leave",Node == "N10" ? "不采用这次采访" : "结束访问 · 用一段"));
            if (Node == "N51") c.Add(("cancel_pending","返回交涉 · 取消待确认交易"));
            if (Node == "result") c.Add(("continue","读完材料，继续"));
            if (Node == "N80") { c.Add(("edit","返回改写 · 保留原句")); c.Add(("signoff","继续到签发确认")); }
            if (Node == "N81") { c.Add(("edit","返回改写")); c.Add(("publish","确认签发这一版")); }
            if (Node == "N82") { c.Add(("edit","回到标题")); c.Add(("hold","确认本版暂缓")); }
            if (Node == "N90" || new[] {"N91","N92","N93","N94","N95","N96","aftermath"}.Contains(Node)) c.Add(("continue","继续"));
            return c;
        }
        public void Choose(string choice)
        {
            if (choice == "hold_review" && Node == "N70")
            { Record(choice); ClearHeadlineReview(); Node = "N82"; return; }
            if (!Choices().Any(x => x.id == choice)) throw new InvalidOperationException("Choice unavailable: " + choice);
            if (choice == "signoff" || choice == "publish") ValidateHeadlineReview();
            string before = Node; Record(choice); ResultText = "";
            switch (choice)
            {
                case "begin": Node = "N10"; break;
                case "cancel_entry": entryScene = null; Node = "N20"; break;
                case "enter": activeScene = entryScene; entryScene = null; Node = SceneNodes[activeScene]; break;
                case "desk": Node = "desk_confirm"; break;
                case "cancel_desk": Node = "N20"; break;
                case "finish_investigation": Slots = 0; Node = "N70"; break;
                case "cancel_pending": pending = null; Node = "N50"; break;
                case "save_video": Grant(Video); Settle(); Result("你把画面停在两边动作之间的那几秒。屏幕没有替你决定怎样写。"); break;
                case "leave":
                    string text = before == "N10" ? "阿岑：那你查到以后再决定。别把没记下来的话写成采访。" :
                        before == "N40" ? "阿岑：那就把你现在确实知道的写清楚。" :
                        before == "N50" ? "许先生：好。你没有拿到这页，别把它写成你看过的记录。" :
                        before == "N60" ? "许先生：那就写你手里有的。" : "本次现场访问结束，未取得影像记录。";
                    Settle(); Result(text); break;
                case "edit": ClearHeadlineReview(); Node = "N70"; break;
                case "signoff": Node = "N81"; break;
                case "publish": Publish(); break;
                case "hold":
                    Ending = "N96"; OutcomeText = S(data["copy"]?["held"]) + "\n\n" +
                        (evidence.Count > 0 ? "你把本局材料按取得顺序收拢。它们还在，今天的调查机会已经结束。" : "桌上没有新的记录。工作单留下两个调查方向，今晚没有替它们填上答案。");
                    Node = "N96"; break;
                case "continue":
                    if (before == "result") Node = Slots > 0 ? "N20" : "N70";
                    else if (before == "N90") Node = Ending;
                    else if (new[] {"N91","N92","N93","N94","N95"}.Contains(before)) Node = "aftermath";
                    else Node = "N99";
                    break;
                default:
                    if (choice.StartsWith("visit:")) { entryScene = choice.Substring(6); Node = "entry"; }
                    break;
            }
        }
        void ClearHeadlineReview() { reviewedClaims = null; reviewedText = null; reviewedBasis = null; }
        public bool PrepareHeadline(string text)
        {
            if (Node != "N70") throw new InvalidOperationException("Not at editor");
            Draft = text; ClearHeadlineReview(); HeadlineMessage = "";
            var item = ((JObject)data["headlines"]).Properties().Select(p => p.Value)
                .FirstOrDefault(h => S(h["text"]) == text.Trim());
            if (item == null || item["claims"] == null)
            { HeadlineMessage = "原句已保留。当前脚本没有完整可执行的理解，请改写或选择另一版作者选稿。"; return false; }
            var claims = (JArray)item["claims"];
            if (!ValidHeadline(claims))
            { HeadlineMessage = "原句已保留。完整标题中有当前尚未开放的含义或来源，整版尚不能签发。"; return false; }
            Record("review_headline", text);
            reviewedText = text; reviewedClaims = (JArray)claims.DeepClone();
            reviewHistoryCount = history.Count; reviewedBasis = HeadlineBasis(); Node = "N80";
            return true;
        }
        bool ValidHeadline(JArray claims)
        {
            if (claims == null) return false;
            foreach (JObject c in claims)
            {
                string target = S(c["target_id"]), source = S(c["source_ref_id"]);
                var def = data["targets"]?[target];
                if (def == null || !B(def["headline"]) || !Has(def["values"], S(c["value_id"])) ||
                    !new[] {"AFFIRM","DENY"}.Contains(S(c["polarity"])) ||
                    !new[] {"ASSERTED","SPECULATIVE","QUESTIONED"}.Contains(S(c["commitment_mode"])) ||
                    !Arr(def["headline_requires"]).All(e => evidence.ContainsKey(S(e)))) return false;
                if (source.Length > 0 && (!sources.Contains(source) ||
                    !(target == Fire || target == View) || S(c["commitment_mode"]) != "ASSERTED")) return false;
            }
            return true;
        }
        string HeadlineBasis() => new JObject
        {
            ["evidence"] = JObject.FromObject(evidence), ["sources"] = new JArray(sources.OrderBy(x => x)),
            ["cooperation"] = JObject.FromObject(cooperation),
            ["state"] = new JObject { ["Money"] = Money, ["Reputation"] = Reputation,
                ["Threat Level"] = ThreatLevel, ["Public Opinion"] = PublicOpinion },
            ["versions"] = Versions()
        }.ToString(Formatting.None);
        JObject Versions() => new JObject { ["version"] = S(data["version"]),
            ["catalogue_version"] = S(data["catalogue_version"]),
            ["support_version"] = S(data["support_version"]),
            ["consequences_version"] = S(data["consequences_version"]) };
        JArray ValidateHeadlineReview()
        {
            if (reviewedClaims == null || reviewedBasis != HeadlineBasis() || !ValidHeadline(reviewedClaims) ||
                history.Skip(reviewHistoryCount).Any(h => !new[] {"signoff","publish"}.Contains(S(h["action"]))))
                throw new InvalidOperationException("Headline review stale or invalid");
            return reviewedClaims;
        }
        public JArray EvaluateClaims(JArray claims)
        {
            var result = new JArray();
            foreach (JObject c in claims)
            {
                var rows = Arr(data["relationships"]).Cast<JObject>().Where(r =>
                    Arr(r["requires_evidence"]).All(e => evidence.ContainsKey(S(e))) &&
                    S(r["target_id"]) == S(c["target_id"]) && S(r["value_id"]) == S(c["value_id"])).ToArray();
                var underlying = rows.Where(r => S(r["dimension"]) == "UNDERLYING").ToArray();
                var supporting = underlying.Where(r => S(r["polarity"]) == S(c["polarity"])).Select(r => S(r["id"])).ToArray();
                var contradicting = underlying.Where(r => S(r["polarity"]) != S(c["polarity"])).Select(r => S(r["id"])).ToArray();
                var attribution = rows.Where(r => S(r["dimension"]) == "ATTRIBUTION" &&
                    S(r["polarity"]) == S(c["polarity"]) && S(r["source_ref_id"]) == S(c["source_ref_id"]))
                    .Select(r => S(r["id"])).ToArray();
                result.Add(new JObject { ["underlying"] = contradicting.Length > 0 ? "CONTRADICTED" :
                    supporting.Length > 0 ? "SUPPORTED" : "INSUFFICIENT",
                    ["attribution"] = S(c["source_ref_id"]).Length == 0 ? "NOT_APPLICABLE" :
                        attribution.Length > 0 ? "SUPPORTED" : "INSUFFICIENT",
                    ["supporting_relationships"] = new JArray(supporting),
                    ["contradicting_relationships"] = new JArray(contradicting),
                    ["attribution_relationships"] = new JArray(attribution) });
            }
            return result;
        }
        void Publish()
        {
            var claims = (JArray)ValidateHeadlineReview().DeepClone();
            var evaluations = EvaluateClaims(claims);
            publication = new JObject { ["headline"] = reviewedText, ["claims"] = claims.DeepClone(),
                ["evidence"] = JObject.FromObject(evidence), ["source_ids"] = new JArray(sources.OrderBy(x => x)),
                ["evaluations"] = evaluations.DeepClone(), ["versions"] = Versions(),
                ["prior_events"] = new JArray(events.Select(e => e.DeepClone())),
                ["cooperation"] = JObject.FromObject(cooperation) };
            var issues = new List<(int index,string kind)>();
            bool qualifier = claims.Cast<JObject>().Select((c,i) => (c,i)).Any(x =>
                S(x.c["target_id"]) == View && S(x.c["polarity"]) == "DENY" &&
                S(evaluations[x.i]["underlying"]) == "SUPPORTED");
            for (int i = 0; i < claims.Count; i++)
            {
                var c = claims[i]; var e = evaluations[i]; string target = S(c["target_id"]);
                if (S(c["source_ref_id"]).Length > 0)
                {
                    if (S(e["attribution"]) != "SUPPORTED") issues.Add((i,"wrong_attribution"));
                    else if (target == Fire && S(c["value_id"]) == "SECURITY_FORCES" &&
                        S(c["polarity"]) == "AFFIRM" && evidence.ContainsKey(Clarification) && !qualifier)
                        issues.Add((i,"omitted_clarification"));
                }
                else if (S(e["underlying"]) == "CONTRADICTED")
                    issues.Add((i,S(c["commitment_mode"]) == "ASSERTED" ? "contradicted_assertion" : "contradicted_question"));
                else if (S(c["commitment_mode"]) == "ASSERTED" && S(e["underlying"]) == "INSUFFICIENT")
                    issues.Add((i,"insufficient_assertion"));
            }
            if (claims.Count == 0) Ending = "N95";
            else if (issues.Count > 0) Ending = "N94";
            else if (claims.Cast<JObject>().Select((c,i)=>(c,i)).Any(x =>
                S(x.c["source_ref_id"]).Length > 0 && S(evaluations[x.i]["underlying"]) != "SUPPORTED" &&
                !(S(x.c["target_id"]) == Fire && S(x.c["value_id"]) == "SECURITY_FORCES" &&
                  S(x.c["polarity"]) == "AFFIRM" && qualifier))) Ending = "N92";
            else if (claims.Cast<JObject>().Any(c => S(c["commitment_mode"]) != "ASSERTED")) Ending = "N93";
            else Ending = "N91";
            ComposeConsequences(claims, evaluations, issues);
            if (Ending == "N91") Event("professional_followup");
            if (Ending == "N94") Event("editorial_review");
            Node = "N90";
        }
        void ComposeConsequences(JArray claims, JArray evaluations, List<(int index,string kind)> issues)
        {
            var copy = data["copy"];
            var topics = new HashSet<string>(claims.Cast<JObject>().Select(c => S(c["target_id"])));
            bool fire = topics.Contains(Fire) || topics.Contains(View), funding = topics.Contains(Funding) || topics.Contains(Uses);
            var parts = new List<string>(); var people = new List<string>();
            var supported = claims.Cast<JObject>().Select((c,i)=>(c,i)).Where(x =>
                S(evaluations[x.i]["underlying"]) == "SUPPORTED" && S(x.c["commitment_mode"]) == "ASSERTED" &&
                new[] {"SUPPORTED","NOT_APPLICABLE"}.Contains(S(evaluations[x.i]["attribution"]))).ToArray();
            Action<string> add = key => parts.Add(S(copy[key]));
            if (Ending == "N91")
            {
                if (claims.Cast<JObject>().Any(c => S(c["target_id"]) == Fire && S(c["source_ref_id"]).Length == 0)) add("supported_fire");
                if (topics.Contains(View)) { add("supported_view"); if (claims.Cast<JObject>().Any(c => S(c["target_id"]) == Fire && S(c["source_ref_id"]).Length > 0)) add("historical_quote"); }
                if (topics.Contains(Funding)) add("supported_payment");
                if (topics.Contains(Uses)) add("supported_uses");
                if (fire) add("reader_fire"); if (funding) add("reader_payment");
                add("professional_followup");
            }
            else if (Ending == "N92") add(evidence.ContainsKey(Video) ? "contested_with_video" : "contested_without_video");
            else if (Ending == "N93")
            {
                var questions = claims.Cast<JObject>().Select((c,i)=>(c,i)).Where(x => S(x.c["commitment_mode"]) != "ASSERTED").ToArray();
                add(questions.Any(x => S(evaluations[x.i]["underlying"]) == "INSUFFICIENT") ? "question_without_record" : "question_with_record");
                foreach (var q in questions) parts.Add(DescribeClaim(q.c) +
                    (S(evaluations[q.i]["underlying"]) == "INSUFFICIENT" ? "：这项尚未取得对应记录。" : "：这项已有对应记录。"));
            }
            else if (Ending == "N94")
            {
                add("review_open");
                foreach (var issue in issues) parts.Add(DescribeClaim((JObject)claims[issue.index]) + "\n\n编辑：" + S(copy[issue.kind]));
                if (supported.Length > 0) add("keep_supported");
                if (issues.Any(x => x.kind == "wrong_attribution")) add("source_correction");
                if (funding) add("funding_review"); if (fire) add("fire_review"); add("review_close");
            }
            else add("no_claim");
            if ((Ending == "N92" || Ending == "N93") && supported.Length > 0)
            {
                add("keep_other_claims");
                foreach (var x in supported)
                {
                    var rows = Arr(data["relationships"]).Cast<JObject>().Where(r =>
                        Arr(evaluations[x.i]["supporting_relationships"]).Any(y => S(y) == S(r["id"])) ||
                        Arr(evaluations[x.i]["contradicting_relationships"]).Any(y => S(y) == S(r["id"])) ||
                        Arr(evaluations[x.i]["attribution_relationships"]).Any(y => S(y) == S(r["id"])));
                    var basis = rows.SelectMany(r => Arr(r["requires_evidence"]).Select(S)).Distinct().OrderBy(y => y)
                        .Where(evidence.ContainsKey).Select(id => S(evidence[id]["title"]));
                    parts.Add(DescribeClaim(x.c) + "；留存材料：" + string.Join("、", basis));
                }
            }
            if (fire)
            {
                if (issues.Any(x => x.kind == "wrong_attribution")) { }
                else if (!cooperation["witness"]) people.Add(S(copy["witness_closed"]));
                else if (issues.Any(x => x.kind == "omitted_clarification")) people.Add(S(copy["witness_omitted"]));
                else if (evidence.ContainsKey(Clarification)) people.Add(S(copy[supported.Any(x => S(x.c["target_id"]) == View && S(x.c["polarity"]) == "DENY") ? "witness_clarified" : "witness_kept"]));
                else if (evidence.ContainsKey(Audio)) people.Add(S(copy["witness_open"]));
            }
            bool fundingIssue = issues.Any(x => new[] {Funding,Uses}.Contains(S(claims[x.index]["target_id"])));
            if (funding && !fundingIssue)
            {
                if (Ending == "N92" || Ending == "N93") people.Add(S(copy["company_question"]));
                if (!cooperation["clerk"]) people.Add(S(copy[evidence.ContainsKey(Ledger) ? "clerk_closed_with_ledger" : "clerk_closed_no_ledger"]));
                else if (evidence.ContainsKey(Context)) people.Add(S(copy[topics.Contains(Uses) ? "uses_published" : "uses_known"]));
                else if (evidence.ContainsKey(Ledger)) people.Add(S(copy["uses_unknown"]));
            }
            OutcomeText = string.Join("\n\n", parts);
            PeopleText = people.Count > 0 ? string.Join("\n\n", people) : "没有新增来源回应；本版没有替你取得新的材料。";
        }
        public static string DescribeClaim(JObject claim)
        {
            string target = S(claim["target_id"]), value = S(claim["value_id"]);
            string text = target == Fire ? (value == "MILITIA" ? "民兵在主通道率先开火" : "安保在主通道率先开火") :
                target == Funding ? "Company A 为本次行动提供资金" : target == View ? "阿岑在首枪发生时看见了开火来源" :
                "R17 行动账目列明车辆、照明与临时劳务";
            if (S(claim["polarity"]) == "DENY") text = "否定“" + text + "”";
            if (S(claim["source_ref_id"]).Length > 0) text = "目击者说过：" + text;
            string mode = S(claim["commitment_mode"]);
            return (mode == "ASSERTED" ? "明确陈述：" : mode == "SPECULATIVE" ? "猜测：" : "提问：") + text;
        }
        public string NodeTitle => S(data["nodes"]?[Node]?["title"]);
        public string NodeText => S(data["nodes"]?[Node]?["text"])
            .Replace("{slots}", Slots.ToString())
            .Replace("{money}", Money.ToString())
            .Replace("{after_money}", (Money - 500).ToString());
        public IReadOnlyDictionary<string, string> Backgrounds() => data["nodes"]?[Node]?["background"] is JObject o ?
            o.Properties().ToDictionary(p => p.Name, p => S(p.Value)) : new Dictionary<string,string>();
        public string ReviewedHeadline => reviewedText;
        public JArray ReviewedClaims => reviewedClaims == null ? null : (JArray)reviewedClaims.DeepClone();
        public string Pending => pending;
        public string EntryScene => entryScene;
        public string ActiveScene => activeScene;
    }
}
