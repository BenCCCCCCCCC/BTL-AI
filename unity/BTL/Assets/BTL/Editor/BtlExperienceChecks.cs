using System;
using System.Linq;
using BTL;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEngine;

public static class BtlExperienceChecks
{
    static string Content(string file)=>AssetDatabase.LoadAssetAtPath<TextAsset>("Assets/BTL/Content/Generated/"+file).text;
    static ChapterSession Start()
    {
        var s=new ChapterSession(Content(BtlProductionTools.ChapterFile));
        s.Choose("begin");Say(s,"record");s.Choose("continue");return s;
    }
    static ChapterPresentation View(ChapterSession s)=>new ChapterPresentation(s,Content(BtlProductionTools.PresentationFile));
    static void Need(bool ok,string note){if(!ok)throw new Exception("BTL U5: "+note);}
    static void Say(ChapterSession s,string id)
    {
        var flow=new ChapterInterview(s);
        flow.Prepare(ChapterSession.S(s.AvailableScripts().Single(x=>ChapterSession.S(x["id"])==id)["text"]));flow.Confirm();
    }
    static void Visit(ChapterSession s,string scene){s.Choose("visit:"+scene);s.Choose("enter");}
    static void Publish(ChapterSession s,string id)
    {
        if(s.Node=="N20"){s.Choose("desk");s.Choose("finish_investigation");}
        Need(s.PrepareHeadline(ChapterSession.S(s.Data["headlines"][id]["text"])),"authored headline prepares");
        s.Choose("signoff");s.Choose("publish");
    }
    [MenuItem("BTL/Check U5 Experience Changes")]
    public static void Run()
    {
        // Changed content/version and read-only scene selection, not a repeat of the U1 rule suite.
        var a=Start();Visit(a,"A");a.Choose("save_video");a.Choose("continue");
        Visit(a,"B");Say(a,"offer500");Say(a,"accept");a.Choose("continue");
        string tradeoff=View(a).Tradeoff("S-A");
        Need(tradeoff.Contains("把科目问清楚")&&!tradeoff.Contains("车辆"),"last-slot opportunity uses only open questions");
        Visit(a,"S-A");Say(a,"position");a.Choose("continue");Publish(a,"H11");
        var av=View(a);int rev=a.Revision;int events=a.Events.Count;
        Need(av.Aftermath().Any(x=>x.actor=="witness"&&x.text.Contains("明早")),"clarification has personal callback");
        Need(!av.Aftermath().Any(x=>x.actor=="clerk"),"unpublished funding topic gets no clerk response");
        Need(a.Revision==rev,"reading scenes is read only");
        var snapshot=a.Publication;
        ChapterUI.FinishReading(a);
        Need(a.Finished&&a.Events.Count==events&&JToken.DeepEquals(snapshot,a.Publication),"merged reading keeps publication/effects");
        Need(av.Recap().Any(x=>x.body.Contains("明天还要见")),"accepted response keeps new character detail");

        var b=Start();Visit(b,"B");Say(b,"offer500");Say(b,"accept");b.Choose("continue");
        Visit(b,"S-B");Say(b,"codes");b.Choose("continue");Publish(b,"H10");
        Need(View(b).Aftermath().Any(x=>x.actor=="clerk"&&x.text.Contains("同号两页")),"funding scope scene matches actual response");
        Need(!View(b).Aftermath().Any(x=>x.actor=="witness"),"funding-only story invents no witness contact");

        // Same acquired clarification, different authored choice: scene must not praise an omission.
        var omitted=Start();Visit(omitted,"A");omitted.Choose("save_video");omitted.Choose("continue");
        Visit(omitted,"S-A");Say(omitted,"position");omitted.Choose("continue");Publish(omitted,"H3");
        Need(omitted.Ending=="N94"&&View(omitted).Aftermath().Any(x=>x.text.Contains("为什么报纸上"))&&
            !View(omitted).Aftermath().Any(x=>x.text.Contains("至少这次")),"omitted clarification gets its actual objection");

        var held=Start();held.Choose("desk");held.Choose("finish_investigation");held.Choose("hold_review");held.Choose("hold");
        Need(View(held).Aftermath().Count()==1&&View(held).Aftermath().Single().actor=="editor","hold invents no publication contacts");
        ChapterUI.FinishReading(held);Need(held.Finished&&held.Publication==null&&held.Events.Count==0,"hold reading reaches archive without publication");
        Debug.Log("BTL U5 EXPERIENCE CHANGES PASSED: new content, last-slot tradeoff, actual-response staging, omission, merged reading and hold.");
    }
}
