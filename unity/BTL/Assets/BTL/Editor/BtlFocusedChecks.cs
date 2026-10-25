using System;
using System.Linq;
using BTL;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEngine;

public static class BtlFocusedChecks
{
    static string Json => AssetDatabase.LoadAssetAtPath<TextAsset>(
        "Assets/BTL/Content/Generated/railyard_chapter.v1.0.json").text;
    static void Need(bool ok, string message) { if (!ok) throw new Exception("BTL U1 check failed: " + message); }
    static void Choose(ChapterSession s, string id) => s.Choose(id);
    static void Interview(ChapterSession s, string id)
    {
        var script = s.AvailableScripts().First(x => ChapterSession.S(x["id"]) == id);
        var flow = new ChapterInterview(s);
        Need(flow.Prepare(ChapterSession.S(script["text"])), "prepare " + id);
        Need(flow.ReviewLines().Count >= 3, "complete review " + id);
        flow.Confirm();
    }
    static ChapterSession Start()
    {
        var s = new ChapterSession(Json); Choose(s,"begin"); Interview(s,"record"); Choose(s,"continue"); return s;
    }
    static void Visit(ChapterSession s, string scene)
    { Choose(s,"visit:" + scene); Choose(s,"enter"); }
    static void Desk(ChapterSession s)
    { if (s.Node == "N20") { Choose(s,"desk"); Choose(s,"finish_investigation"); } Need(s.Node == "N70","editor"); }
    static void Publish(ChapterSession s, string id)
    {
        Desk(s);
        Need(s.PrepareHeadline(ChapterSession.S(s.Data["headlines"][id]["text"])),"headline " + id);
        Choose(s,"signoff"); Choose(s,"publish");
    }
    [MenuItem("BTL/Run U1 Focused Checks")]
    public static void Run()
    {
        // Review remains inert; stale and edited candidates cannot execute.
        var stage = new ChapterSession(Json); Choose(stage,"begin");
        var flow = new ChapterInterview(stage);
        string line = ChapterSession.S(stage.AvailableScripts().First()["text"]);
        int revision = stage.Revision;
        Need(!flow.Prepare("他说的那个呢？"),"ambiguous blocked");
        Need(!flow.Prepare("脚本外原句"),"unknown line blocked");
        Need(flow.Draft == "脚本外原句" && stage.Revision == revision && stage.Evidence.Count == 0,"failure keeps draft and reality");
        Need(flow.Prepare(line),"record prepared"); flow.Edit();
        bool rejected = false; try { flow.Confirm(); } catch (InvalidOperationException) { rejected = true; }
        Need(rejected && stage.Evidence.Count == 0,"rewrite cancels review");
        Need(flow.Prepare(line),"record prepared again"); stage.Background("你希望我们怎么写？");
        rejected = false; try { flow.Confirm(); } catch (InvalidOperationException) { rejected = true; }
        Need(rejected && stage.Evidence.Count == 0,"revision invalidates review");

        // Main U2 route: initial recording, offer, explicit payment, H4, signoff and once-only consequence.
        var s = Start(); Need(s.Evidence.ContainsKey(ChapterSession.Audio),"E1");
        Visit(s,"B"); Interview(s,"offer500");
        Need(s.Money == 600 && !s.Evidence.ContainsKey(ChapterSession.Ledger) && s.Pending != null,"offer is pending");
        Need(s.NodeText.Contains("当前 600，付款后 100") && !s.NodeText.Contains("{money}"),"payment copy resolves values");
        Interview(s,"accept"); Need(s.Money == 100 && s.Evidence.ContainsKey(ChapterSession.Ledger) && s.Slots == 2,"payment and E3");
        Choose(s,"continue"); Publish(s,"H4");
        Need(s.Ending == "N91" && s.Reputation == 1 && s.PublicOpinion == 0,"H4 outcome");
        Need(s.Publication != null && ((JArray)s.Publication["claims"]).Count == 1,"frozen claim");
        Need(((JObject)s.Publication["evidence"]).Property(ChapterSession.Ledger) != null,"snapshot evidence");
        Need(((JObject)s.Publication["versions"]).Properties().Count() == 4,"four versions");
        var leakedCopy = s.Publication; leakedCopy["headline"] = "外部篡改";
        Need(ChapterSession.S(s.Publication["headline"]) != "外部篡改","publication read is defensive");
        Need(ChapterSession.DescribeClaim((JObject)((JArray)s.Publication["claims"])[0]).Contains("明确陈述"),"Chinese claim summary");
        Need(s.Events.Count(x => ChapterSession.S(x["id"]) == "ledger_purchase") == 1 &&
             s.Events.Count(x => ChapterSession.S(x["id"]) == "professional_followup") == 1,"events once");
        rejected = false; try { Choose(s,"publish"); } catch (InvalidOperationException) { rejected = true; }
        Need(rejected && s.Money == 100 && s.Reputation == 1,"cannot publish twice");
        Choose(s,"continue"); Choose(s,"continue"); Choose(s,"continue"); Need(s.Finished,"ending closed");

        var hold = Start(); Desk(hold);
        Need(!hold.PrepareHeadline("自己写的未接通标题") && hold.Node == "N70" && hold.Draft.Length > 0,"unknown title kept");
        Need(!hold.PrepareHeadline(ChapterSession.S(hold.Data["headlines"]["H10"]["text"])),"unavailable full title blocked");
        Choose(hold,"hold_review"); Choose(hold,"hold");
        Need(hold.Ending == "N96" && hold.Publication == null && hold.Reputation == 0,"hold has no publication");

        var contested = Start(); Visit(contested,"A"); Choose(contested,"save_video"); Choose(contested,"continue");
        Publish(contested,"H3"); Need(contested.Ending == "N92","old quote contested after video");
        var clarified = Start(); Visit(clarified,"A"); Choose(clarified,"save_video"); Choose(clarified,"continue");
        Visit(clarified,"S-A"); Interview(clarified,"position"); Choose(clarified,"continue");
        Publish(clarified,"H3"); Need(clarified.Ending == "N94" && clarified.Reputation == -1,"omitted clarification review");
        var noClaim = Start(); Publish(noClaim,"H8");
        Need(noClaim.Ending == "N95" && noClaim.Publication != null && ((JArray)noClaim.Publication["claims"]).Count == 0,"zero-claim publication");

        Debug.Log("BTL U1 focused checks passed: staged interview, funding/H4, atomic headline, hold, clarification, zero-claim.");
    }
}
