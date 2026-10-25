using System;
using System.Linq;
using Newtonsoft.Json.Linq;
using UnityEngine;
using UnityEngine.UIElements;

namespace BTL
{
    [RequireComponent(typeof(UIDocument))]
    public sealed class ChapterUI : MonoBehaviour
    {
        public TextAsset chapter, presentation;
        public StyleSheet styleSheet;
        public Font chineseFont;
        public UnityEngine.TextCore.Text.FontAsset chineseSdf;
        public Texture2D desk, yard, records, editorPortrait, witnessPortrait, clerkPortrait;
        ChapterSession session;
        ChapterInterview interview;
        ChapterPresentation story;
        VisualElement root, main, side;
        ScrollView mainScroll;
        Label errorLabel;
        TextField draftInput;
        string headlineDraft = "", selectedEvidence, headlineGroup = "现场", entryTradeoff = "";
        bool chooseScript = true, chooseHeadline = true, editOriginal, focusDraft, focusFeedback;
        VisualElement feedback;
        int fontStep;
        float FontScale => new[] {1f,1.25f,1.5f}[fontStep];
        public ChapterSession Session => session;
        void Awake() { Application.targetFrameRate=60; fontStep=Mathf.Clamp(PlayerPrefs.GetInt("btl.textSize",0),0,2); Restart(); }
        void OnEnable() { if(session!=null) Render(); }
        void Restart()
        {
            session=new ChapterSession(chapter.text); interview=new ChapterInterview(session);
            story=new ChapterPresentation(session,presentation.text);
            headlineDraft="";selectedEvidence=null;chooseScript=chooseHeadline=true;editOriginal=false;
        }
        VisualElement Box(VisualElement parent,string css)
        {var e=new VisualElement();e.AddToClassList(css);parent.Add(e);return e;}
        Label Text(VisualElement parent,string value,string css="body")
        {
            var e=new Label(story.Display(value));e.AddToClassList(css);e.enableRichText=false;
            e.selection.isSelectable=true;
            float scale=parent.ClassListContains("topbar")||parent.ClassListContains("person")||parent.ClassListContains("status")?1:FontScale;
            e.style.fontSize=(css=="heading"?29:css=="title"?23:css=="small"?18:22)*scale;
            parent.Add(e);return e;
        }
        void Prose(VisualElement parent,string value)
        {foreach(var p in (value??"").Split(new[]{"\n\n"},StringSplitOptions.RemoveEmptyEntries)) Text(parent,p);}
        Button Button(VisualElement parent,string label,Action action,bool primary=false,string name=null,bool redraw=true)
        {
            var b=new Button(()=>Guard(action,redraw)){text=label,name=name};
            b.RegisterCallback<KeyDownEvent>(e=>
            {
                if(e.keyCode!=KeyCode.Return&&e.keyCode!=KeyCode.KeypadEnter&&e.keyCode!=KeyCode.Space)return;
                e.StopImmediatePropagation();Guard(action,redraw);
            },TrickleDown.TrickleDown);
            b.RegisterCallback<NavigationSubmitEvent>(e=>e.StopImmediatePropagation(),TrickleDown.TrickleDown);
            b.AddToClassList(primary?"primary":"action");b.style.fontSize=18*(parent.ClassListContains("topbar")?1:FontScale);parent.Add(b);return b;
        }
        void Guard(Action action,bool redraw=true)
        {
            string node=session.Node;
            try
            {
                action();
                if(node!=session.Node){interview=new ChapterInterview(session);chooseScript=true;editOriginal=false;}
                if(redraw)Render();
            }
            catch(Exception e)
            {
                if(errorLabel!=null)errorLabel.text="当前操作尚未执行。请返回修改后再确认。";
                Debug.LogWarning("BTL input refused: "+e.Message);
            }
        }
        void Render()
        {
            root=GetComponent<UIDocument>().rootVisualElement;
            root.Clear();root.styleSheets.Clear();root.styleSheets.Add(styleSheet);
            root.AddToClassList("chapter-root");root.style.unityFontDefinition=FontDefinition.FromSDFFont(chineseSdf);
            var top=Box(root,"topbar");
            Text(top,"字里行间  /  货场调查","title");
            Text(top,"调查  —  写作  —  余波  —  归档","small").AddToClassList("stages");
            Button(top,"字号 "+new[]{"标准","较大","最大"}[fontStep],()=>
            {fontStep=(fontStep+1)%3;PlayerPrefs.SetInt("btl.textSize",fontStep);},name:"text-size");
            Button(top,"退出试玩",QuitDialog,redraw:false);
            var hero=Box(root,"hero");
            var picture=new Image{image=story.Scene=="yard"?yard:story.Scene=="records"?records:desk,scaleMode=ScaleMode.ScaleToFit};
            picture.AddToClassList("scene-image");hero.Add(picture);
            var veil=Box(hero,"hero-veil");
            var portrait=new Image{image=story.Actor=="witness"?witnessPortrait:story.Actor=="clerk"?clerkPortrait:editorPortrait,scaleMode=ScaleMode.ScaleToFit};
            portrait.AddToClassList("portrait");bool atMonitor=story.SourceNode=="N30";
            if(!atMonitor)veil.Add(portrait);
            var who=Box(veil,"person");var person=story.Data["characters"][story.Actor];
            string role=ChapterSession.S(person["role"]);
            if(session.Ending!=null)role=session.Publication==null?"报社 · 本版暂缓":"报社 · 印刷之后";
            Text(who,atMonitor?"货场 · 主通道影像":role,"small");
            Text(who,atMonitor?"现场笔记":ChapterSession.S(person["name"]),"heading");
            Text(who,atMonitor?"先留存这段经过，再决定这一版怎样写。":ChapterSession.S(person["note"]),"small");
            var status=Box(root,"status");
            Text(status,$"{story.Stage}  ·  剩余 {session.Slots} 段调查  ·  经费 {session.Money}","small");
            Text(status,"阅读与改稿不耗时  /  离线脚本 · 关闭后不保存","small");
            var columns=Box(root,"columns");
            mainScroll=new ScrollView(ScrollViewMode.Vertical);mainScroll.AddToClassList("main-scroll");columns.Add(mainScroll);main=mainScroll.contentContainer;
            var dossier=new ScrollView(ScrollViewMode.Vertical);dossier.AddToClassList("dossier");columns.Add(dossier);side=dossier.contentContainer;
            draftInput=null;feedback=null;RenderMain();RenderSide();
            if(focusDraft&&draftInput!=null)
            {var target=draftInput;focusDraft=false;mainScroll.schedule.Execute(()=>{mainScroll.ScrollTo(target);target.Focus();}).ExecuteLater(50);}
            if(focusFeedback&&feedback!=null)
            {var target=feedback;focusFeedback=false;mainScroll.schedule.Execute(()=>mainScroll.ScrollTo(target)).ExecuteLater(50);}
        }
        string Title()
        {
            switch(session.Node)
            {
                case "entry":return ChapterSession.S(story.Data["investigations"][session.EntryScene]["title"]);
                case "desk_confirm":return "把调查带回编辑台";
                case "result":return "留下这次访问的记录";
                case "N70":return "这一版，准备回答什么？";
                case "N80":return "逐项复核这句话";
                case "N81":return "把这一版交给读者";
                case "N82":return "决定暂缓之前";
                case "N90":return "报纸刊出之后";
                case "aftermath":return "他们接下来怎么回应";
                case "N99":return "这一晚，你留下了什么";
                default:return session.Ending==session.Node?story.EndingTitle:session.NodeTitle;
            }
        }
        void RenderMain()
        {
            string n=session.Node;Text(main,Title(),"heading");
            if(n=="N99"){RenderArchive();return;}
            if(n=="N20"){RenderInvestigations();return;}
            if(n=="N90"||n=="N96"){RenderAftermath();return;}
            if(n=="entry")
            {
                Text(main,ChapterSession.S(story.Data["investigations"][session.EntryScene]["question"]));
                Text(main,ChapterSession.S(story.Data["investigations"][session.EntryScene]["cost"]),"small");
                if(entryTradeoff.Length>0)Text(Box(main,"note"),entryTradeoff);
                Text(main,"进入后，本场结束使用一段调查时间。现在返回不耗时。","small");
            }
            else if(n=="desk_confirm")Text(main,"回到编辑台后，本局调查结束，剩余时间放弃。手里的材料都会保留，标题仍由你决定。");
            else if(n=="result")
            {
                Prose(main,session.ResultText);string id=story.LatestEvidence;
                if(session.Evidence.TryGetValue(id,out var material))
                {
                    var card=Box(main,"material-card");Text(card,"已留存 · "+ChapterSession.S(material["title"]),"title");
                    Prose(card,ChapterSession.S(material["text"]));
                    Text(Box(main,"note"),"记者笔记\n"+story.Note(id));selectedEvidence=id;
                }
            }
            else if(n=="N80"||n=="N81")RenderHeadlineReview();
            else if(n=="N82")Text(main,"这一版将暂缓刊发。没有刊发快照，已取得材料仍能在本局结尾回看。");
            else if(n=="N90"||n=="N96")Prose(main,session.OutcomeText);
            else if(n=="aftermath")Prose(main,session.PeopleText);
            else if(session.Ending==n)Text(main,story.EndingText);
            else
            {
                if(!interview.HasReview&&(!IsInterview(n)||chooseScript)&&(n!="N70"||chooseHeadline))
                {
                    Prose(main,session.NodeText);
                }
                if(n=="N00")
                {
                    Text(main,"离线脚本样章：先选择一句表达，再核对采访意图并确认。编辑原句可保留你的措辞，当前仅能执行预写表达。关闭后不保存。","small");
                }
                if(!interview.HasReview&&chooseScript&&session.ResultText.Length>0&&IsInterview(n))Prose(Box(main,"reply"),session.ResultText);
            }
            if(IsInterview(n))RenderInterview();
            if(n=="N70")RenderHeadline();
            foreach(var c in session.Choices().Where(c=>c.id!="leave"||!IsInterview(n)))
                Button(main,ChoiceLabel(c.id,c.label),()=>{interview.Edit();session.Choose(c.id);},
                    new[]{"begin","enter","continue","signoff","publish","hold"}.Contains(c.id),"choice-"+c.id);
            if(n=="N70")Button(main,"这一版先不刊发",()=>session.Choose("hold_review"),name:"hold-review");
            if(!interview.HasReview&&session.Backgrounds().Count>0)
            {
                var background=new Foldout{text="再聊几句",value=false};main.Add(background);
                foreach(var p in session.Backgrounds())Button(background,p.Key,()=>session.Background(p.Key));
            }
            errorLabel=Text(main,"","small");errorLabel.AddToClassList("error");
        }
        static bool IsInterview(string n)=>new[]{"N10","N40","N50","N51","N60"}.Contains(n);
        string ChoiceLabel(string id,string fallback)
        {
            if(id=="continue")return session.Node=="N90"?"看编辑留下的工作单":session.Node=="aftermath"||session.Node=="N96"?"整理本局记录":
                session.Node=="result"?"带着这些记录继续":"听听他们的回应";
            return fallback;
        }
        void RenderInvestigations()
        {
            if(session.Slots==3)Prose(main,session.NodeText);
            if(session.Slots==1)Text(Box(main,"note"),"只够再完成一场访问。把时间交给一个问题，就要把另一个留在今晚之后。阅读和改稿不耗这段时间。");
            foreach(var scene in session.AvailableScenes())
            {
                var info=story.Data["investigations"][scene];var card=Box(main,"route-card");
                Text(card,ChapterSession.S(info["place"]),"small");Text(card,ChapterSession.S(info["question"]));
                Text(card,ChapterSession.S(info["cost"]),"small");
                if(session.Slots==1)Text(card,story.Tradeoff(scene),"small");
                Button(card,ChapterSession.S(info["title"])+" · 一段",()=>
                {entryTradeoff=story.Tradeoff(scene);session.Choose("visit:"+scene);},name:"visit-"+scene);
            }
            foreach(var question in story.OpenQuestions().Where(q=>q.Contains("合作")))Text(main,question,"small");
            Button(main,"结束调查，回到编辑台",()=>session.Choose("desk"),name:"desk");
        }
        void RenderInterview()
        {
            if(interview.HasReview)
            {
                var review=Box(main,"review-card");
                Text(review,string.IsNullOrWhiteSpace(interview.ReviewedOriginal)?"选择：结束这次访问":"你准备说：\n"+interview.ReviewedOriginal,"title");
                Text(review,"采访前，核对我的意思","small");foreach(var line in interview.ReviewLines())Text(review,line);
                Button(main,"返回改写",()=>{interview.Edit();chooseScript=false;editOriginal=true;focusDraft=true;},name:"interview-edit");
                Button(main,"确认，按这句话采访",()=>{interview.Confirm();interview.Edit("");chooseScript=true;},true,"interview-confirm");return;
            }
            Text(main,"准备怎样开口？","title");
            if(chooseScript)
            {
                var scripts=session.AvailableScripts();
                foreach(var script in scripts.Where(s=>s["candidate"]?["tactics"] is JArray t&&t.Count==0&&ChapterSession.S(s["id"])!="ambiguous"))ScriptButton(main,script);
                var other=new Foldout{text=session.Node=="N51"?"其他表达":"施压、质疑或其他表达",value=false};main.Add(other);
                foreach(var script in scripts.Where(s=>((s["candidate"]["tactics"] as JArray)?.Count??0)>0||ChapterSession.S(s["id"])=="ambiguous"))ScriptButton(other,script);
                Text(main,"选卡只准备原句。下一步核对全部意思，确认后才采访；本版使用预写表达。","small");
                if(interview.Draft.Length>0)Button(main,"回到保留的原句",()=>{chooseScript=false;editOriginal=true;focusDraft=true;});
            }
            else
            {
                feedback=Box(main,"selected-expression");Text(feedback,"我的原句","small");Text(feedback,interview.Draft,"title");
                Button(main,"换一种问法",()=>{chooseScript=true;editOriginal=false;});
                if(editOriginal)Input(main,"编辑采访原句",interview.Draft,v=>interview.Edit(v));
                else Button(main,"编辑原句",()=>{editOriginal=true;focusDraft=true;},name:"edit-original");
                if(editOriginal)Text(main,"只有预写原句可执行；其他措辞会保留在草稿里。","small");
                if(interview.Message.Length>0)feedback=Text(Box(main,"note"),interview.Message);
                Button(main,"核对采访意图",()=>{focusFeedback=!interview.Prepare(interview.Draft);},true,"interview-review");
            }
            if(session.Choices().Any(c=>c.id=="leave"))Button(main,"结束本次访问…",()=>interview.PrepareLeave(),name:"interview-leave");
        }
        void ScriptButton(VisualElement parent,JObject script)
        {
            string id=ChapterSession.S(script["id"]);
            Button(parent,ChapterSession.S(script["label"])+"\n“"+ChapterSession.S(script["text"])+"”",()=>
            {interview.Edit(ChapterSession.S(script["text"]));chooseScript=false;editOriginal=false;focusFeedback=true;},name:"script-"+id);
        }
        void Input(VisualElement parent,string label,string value,Action<string> changed)
        {
            var previous=main.Query<Button>().ToList().LastOrDefault();
            Text(parent,label,"small");draftInput=new TextField{multiline=true,value=value,name="original-draft"};
            draftInput.AddToClassList("draft");draftInput.style.fontSize=22*FontScale;
            draftInput.RegisterCallback<KeyDownEvent>(e=>
            {
                if(e.keyCode!=KeyCode.Tab||e.ctrlKey||e.altKey)return;
                var target=e.shiftKey?previous:main.Q<Button>(IsInterview(session.Node)?"interview-review":"headline-review");
                if(target==null)return;
                e.StopImmediatePropagation();target.Focus();mainScroll.ScrollTo(target);
            },TrickleDown.TrickleDown);
            draftInput.RegisterValueChangedCallback(e=>changed(e.newValue));parent.Add(draftInput);
        }
        void RenderHeadline()
        {
            if(chooseHeadline)
            {
                var tabs=Box(main,"tabs");
                foreach(string group in new[]{"现场","资金","其他"})Button(tabs,group,()=>headlineGroup=group,headlineGroup==group);
                foreach(var item in session.VisibleHeadlines().Where(h=>ChapterSession.S(h.Value["group"])==headlineGroup))
                {
                    string text=ChapterSession.S(item.Value["text"]);
                    Button(main,text,()=>{headlineDraft=text;chooseHeadline=false;focusDraft=true;},name:"headline-"+item.Key);
                }
            }
            else Button(main,"比较其他写法",()=>chooseHeadline=true);
            Input(main,"标题原句",headlineDraft,v=>headlineDraft=v);
            Text(main,"可以明确陈述、保留来源归属、提出问题，或暂缓。选稿不代表编辑已认可其中的事实。","small");
            if(session.HeadlineMessage.Length>0)feedback=Text(Box(main,"note"),session.HeadlineMessage);
            Button(main,"核对这句标题的完整意思",()=>{session.PrepareHeadline(headlineDraft);focusFeedback=session.HeadlineMessage.Length>0;},true,"headline-review");
        }
        void RenderHeadlineReview()
        {
            Text(Box(main,"headline-paper"),session.ReviewedHeadline,"title");var claims=session.ReviewedClaims;
            VisualElement meanings=main;
            if(session.Node=="N81")
            {var repeat=new Foldout{text="再次查看标题的完整含义",value=false};main.Add(repeat);meanings=repeat;}
            if(claims.Count==0)Text(meanings,"这句没有具体事实主张。签发它仍是一次刊发。");
            for(int i=0;i<claims.Count;i++)Text(meanings,$"{i+1}. {ChapterSession.DescribeClaim((JObject)claims[i])}");
            if(session.Node=="N80")Text(main,"复核的是整句话。手里有材料，并不意味着每一种写法都有依据。","small");
            if(session.Node=="N81")Text(Box(main,"note"),"确认签发后，这一版文字和当时的材料将一起归档。下一页会呈现编辑、来源和读者的具体回应。");
        }
        void RenderArchive()
        {
            Text(Box(main,"headline-paper"),session.Publication==null?"本版暂缓刊发":ChapterSession.S(session.Publication["headline"]),"title");
            Text(main,story.EndingTitle,"title");Text(main,story.EndingText);
            Text(Box(main,"note"),ChapterSession.S(story.Data["aftermath"]["closing"]));
            var work=new Foldout{text="展开编辑工作单与依据",value=false};main.Add(work);
            foreach(string line in story.WorkSheet())Text(Box(work,"note"),line);
            var open=story.OpenQuestions().ToArray();Text(main,"本局未完成核查","title");
            foreach(string q in open)Text(main,q);
            if(open.Length==0)Text(main,"本局已完成当前开放的核查，报道仍须遵守材料所能说明的范围。");
            var recap=new Foldout{text="回看这次选择",value=false,name="run-recap"};main.Add(recap);int number=0;
            foreach(var item in story.Recap())
            {
                var step=new Foldout{text=$"{++number:00}  {item.title}",value=false};step.AddToClassList("path-step");
                recap.Add(step);Prose(step,item.body);
            }
            var events=new Foldout{text="取证代价与编辑事件",value=false};main.Add(events);
            foreach(var e in session.Events)
            {
                var effects=((JObject)e["effects"]).Properties().Where(p=>p.Value.Value<int>()!=0)
                    .Select(p=>(p.Name=="Money"?"经费":p.Name=="Reputation"?"声誉":p.Name=="Threat Level"?"风险":"公众态度")+" "+p.Value.Value<int>().ToString("+0;-0;0"));
                Text(events,ChapterSession.S(e["label"])+" · "+string.Join("，",effects));
            }
            if(session.Events.Count==0)Text(events,"本局没有产生取证交易、施压或刊发事件。");
            Button(main,"重新开始本案",Restart,true,"restart");Text(main,"只回看本局。重开或退出后，这一局不会保存。","small");
        }
        void RenderAftermath()
        {
            Text(Box(main,"headline-paper"),session.Publication==null?"本版暂缓刊发":ChapterSession.S(session.Publication["headline"]),"title");
            if(session.Publication!=null)Text(main,"第一份样报摊在桌上。机器的声音从走廊传过来。","small");
            foreach(var scene in story.Aftermath())
            {
                var card=Box(main,"aftermath-scene");
                Text(card,ChapterSession.S(story.Data["characters"][scene.actor]["name"]),"title");
                Prose(card,scene.text);
            }
            var records=new Foldout{text="展开原始编辑批注与人物留话",value=false};main.Add(records);
            Prose(records,session.OutcomeText);if(session.Publication!=null)Prose(records,session.PeopleText);
            Button(main,"收好这一版，回看今晚的选择",()=>FinishReading(session),true,"finish-reading");
        }
        public static void FinishReading(ChapterSession current)
        {
            // Submit only the existing reading transitions; publication effects already happened.
            while(new[]{"N90","N91","N92","N93","N94","N95","N96","aftermath"}.Contains(current.Node))
                current.Choose("continue");
        }
        void RenderSide()
        {
            side.Clear();Text(side,session.Publication==null?"随身材料册":"刊发时的材料","title");
            Text(side,"材料正文可选中复制。翻阅不改变当前草稿。","small");
            var materials=session.Publication?["evidence"] as JObject??JObject.FromObject(session.Evidence);
            foreach(var material in materials.Properties())
            {
                string id=material.Name;
                Button(side,ChapterSession.S(material.Value["title"]),()=>{selectedEvidence=id;RenderSide();},selectedEvidence==id,redraw:false);
            }
            if(!materials.Properties().Any())Text(side,"你还没有取得材料。","small");
            if(selectedEvidence!=null&&materials[selectedEvidence]!=null)
            {Text(side,ChapterSession.S(materials[selectedEvidence]["title"]),"title");Prose(side,ChapterSession.S(materials[selectedEvidence]["text"]));}
            else if(materials.Properties().Any())Text(side,"选择一份材料，查看完整记录。","small");
        }
        void QuitDialog()
        {
            var overlay=Box(root,"modal-overlay");var box=Box(overlay,"modal");
            Text(box,"结束今晚的采访？","heading");Text(box,"退出后，本局的草稿、材料和选择不会保存。");
            Button(box,"留在本局",()=>overlay.RemoveFromHierarchy(),redraw:false);
            Button(box,"退出试玩",()=>
            {
#if UNITY_EDITOR
                UnityEditor.EditorApplication.isPlaying=false;
#else
                Application.Quit();
#endif
            },true,redraw:false);
        }
    }
}

