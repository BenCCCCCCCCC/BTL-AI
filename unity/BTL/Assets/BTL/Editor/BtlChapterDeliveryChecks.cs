using System;
using System.Linq;
using BTL;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEngine;

public static class BtlChapterDeliveryChecks
{
    static string Content(string name)=>AssetDatabase.LoadAssetAtPath<TextAsset>("Assets/BTL/Content/Generated/"+name).text;
    static void Need(bool ok,string message){if(!ok)throw new Exception("BTL U3-U4: "+message);}
    static ChapterSession Start()
    {var s=new ChapterSession(Content("railyard_chapter.v1.0.json"));s.Choose("begin");Say(s,"record");s.Choose("continue");return s;}
    static void Say(ChapterSession s,string id)
    {
        var script=s.AvailableScripts().First(x=>ChapterSession.S(x["id"])==id);
        var flow=new ChapterInterview(s);flow.Prepare("  "+ChapterSession.S(script["text"])+"  ");flow.Confirm();
    }
    static void Visit(ChapterSession s,string scene){s.Choose("visit:"+scene);s.Choose("enter");}
    static void Publish(ChapterSession s,string headline)
    {
        if(s.Node=="N20"){s.Choose("desk");s.Choose("finish_investigation");}
        s.PrepareHeadline(ChapterSession.S(s.Data["headlines"][headline]["text"]));s.Choose("signoff");s.Choose("publish");
    }
    static ChapterPresentation View(ChapterSession s)=>new ChapterPresentation(s,Content("railyard_presentation.v1.1.json"));
    [MenuItem("BTL/Check Chapter Presentation")]
    public static void Run()
    {
        // New presentation integration: full clarification route, then funded route.
        var a=Start();Visit(a,"A");a.Choose("save_video");
        Need(View(a).LatestEvidence==ChapterSession.Video && View(a).Note(ChapterSession.Video).Contains("不一样"),"video note uses known audio");
        a.Choose("continue");Visit(a,"S-A");Say(a,"position");a.Choose("continue");
        Need(a.VisibleHeadlines().ContainsKey("H12"),"clarification writing available");
        Publish(a,"H12");
        var v=View(a);int revision=a.Revision;
        var first=v.Recap().ToArray();var work=v.WorkSheet().ToArray();
        Need(first.Any(x=>x.body.Contains("  我会记录")) && first.Any(x=>x.body.Contains("留存：")),"exact accepted original and evidence in recap");
        Need(first.Any(x=>x.body.Contains("阿岑")) && work.Length>=2,"responses and both claims readable");
        Need(v.OpenQuestions().All(x=>!x.Contains("账目科目")),"unopened follow-up not disclosed");
        Need(a.Revision==revision && v.Recap().Count()==first.Length,"recap is read only");
        var b=Start();Visit(b,"B");Say(b,"offer500");Say(b,"accept");b.Choose("continue");
        Visit(b,"S-B");Say(b,"codes");b.Choose("continue");Publish(b,"H10");
        var bv=View(b);
        Need(bv.WorkSheet().Any(x=>x.Contains("支付 500")) && bv.Recap().Any(x=>x.title=="查科目"),"purchase and scope separately recorded");
        Need(!bv.WorkSheet().Any(x=>x.Contains("来源原话与事实经过")),"null source is not a quoted claim");
        Need(bv.Recap().Single(x=>x.title=="签发这一版").body.Contains(b.OutcomeText) &&
            bv.Recap().Single(x=>x.title=="签发这一版").body.Contains(b.PeopleText),"publication recap retains the actual consequences and responses");
        Need(bv.OpenQuestions().All(x=>!x.Contains("科目")),"completed scope not left open");
        var empty=new ChapterSession(Content("railyard_chapter.v1.0.json"));
        Need(View(empty).OpenQuestions().Count()==2 && !View(empty).Recap().Any(),"new run has only known basic directions");
        Debug.Log("BTL U3-U4 presentation checks passed: clarification/H12, ledger scope/H10, read-only recap, exact utterance, no unopened follow-up disclosure.");
    }
}
