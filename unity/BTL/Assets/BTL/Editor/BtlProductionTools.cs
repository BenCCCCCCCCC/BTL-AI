using System;
using System.IO;
using System.Linq;
using BTL;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.UIElements;

public static class BtlProductionTools
{
    const string Root="Assets/BTL/";
    public const string ChapterFile="railyard_chapter.v1.1.json", PresentationFile="railyard_presentation.v1.2.json";
    static string Repo=>Path.GetFullPath(Path.Combine(Application.dataPath,"../../.."));
    [MenuItem("BTL/Prepare Internal Chapter")]
    public static void Prepare()
    {
        if(EditorApplication.isPlaying)throw new InvalidOperationException("Stop Play Mode before preparing assets.");
        foreach(string name in new[]{ChapterFile,PresentationFile})
            File.Copy(Path.Combine(Repo,"ai/content",name),Root+"Content/Generated/"+name,true);
        AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
        foreach(string path in Directory.GetFiles(Root+"Art","*.png"))
        {
            var importer=(TextureImporter)AssetImporter.GetAtPath(path.Replace('\\','/'));
            importer.filterMode=FilterMode.Point;importer.mipmapEnabled=false;
            importer.textureCompression=TextureImporterCompression.Uncompressed;
            importer.npotScale=TextureImporterNPOTScale.None;importer.SaveAndReimport();
        }
        var scene=EditorSceneManager.OpenScene(Root+"Main.unity");
        var view=UnityEngine.Object.FindFirstObjectByType<ChapterUI>();
        view.chapter=AssetDatabase.LoadAssetAtPath<TextAsset>(Root+"Content/Generated/"+ChapterFile);
        view.presentation=AssetDatabase.LoadAssetAtPath<TextAsset>(Root+"Content/Generated/"+PresentationFile);
        view.styleSheet=AssetDatabase.LoadAssetAtPath<StyleSheet>(Root+"UI/Chapter.uss");
        view.chineseFont=AssetDatabase.LoadAssetAtPath<Font>(Root+"Fonts/NotoSansCJKsc-Regular.otf");
        var sdf=AssetDatabase.LoadAssetAtPath<UnityEngine.TextCore.Text.FontAsset>(Root+"Fonts/NotoSansCJKsc-SDF.asset");
        if(sdf==null)
        {
            sdf=UnityEngine.TextCore.Text.FontAsset.CreateFontAsset(view.chineseFont,64,6,
                UnityEngine.TextCore.LowLevel.GlyphRenderMode.SDFAA,2048,2048,
                UnityEngine.TextCore.Text.AtlasPopulationMode.Dynamic,true);
            sdf.name="NotoSansCJKsc-SDF";
            AssetDatabase.CreateAsset(sdf,Root+"Fonts/NotoSansCJKsc-SDF.asset");
            AssetDatabase.AddObjectToAsset(sdf.material,sdf);
            foreach(var texture in sdf.atlasTextures)AssetDatabase.AddObjectToAsset(texture,sdf);
        }
        view.chineseSdf=sdf;
        Func<string,Texture2D> art=n=>AssetDatabase.LoadAssetAtPath<Texture2D>(Root+"Art/"+n+".png");
        view.desk=art("desk");view.yard=art("yard");view.records=art("records");
        view.editorPortrait=art("editor");view.witnessPortrait=art("witness");view.clerkPortrait=art("clerk");
        var doc=view.GetComponent<UIDocument>();
        doc.panelSettings=AssetDatabase.LoadAssetAtPath<PanelSettings>(Root+"MainPanel.asset");
        doc.panelSettings.scaleMode=PanelScaleMode.ScaleWithScreenSize;doc.panelSettings.scale=1;
        doc.panelSettings.referenceResolution=new Vector2Int(1280,800);
        doc.panelSettings.screenMatchMode=PanelScreenMatchMode.MatchWidthOrHeight;
        doc.panelSettings.match=0.5f;
        EditorUtility.SetDirty(doc.panelSettings);EditorUtility.SetDirty(doc);EditorUtility.SetDirty(view);
        EditorSceneManager.MarkSceneDirty(scene);EditorSceneManager.SaveScene(scene);
        EditorBuildSettings.scenes=new[]{new EditorBuildSettingsScene(Root+"Main.unity",true)};
        PlayerSettings.productName="Between the Lines";PlayerSettings.companyName="BTL";
        PlayerSettings.bundleVersion="0.4.0";PlayerSettings.defaultScreenWidth=1280;PlayerSettings.defaultScreenHeight=800;
        PlayerSettings.fullScreenMode=FullScreenMode.Windowed;PlayerSettings.resizableWindow=true;
        AssetDatabase.SaveAssets();
        Debug.Log("BTL U5 assets prepared: chapter 1.1, presentation 1.2, 0.4.0, existing Main/art/font.");
    }
    [MenuItem("BTL/Build Windows Internal")]
    public static void Build()
    {
        if(EditorApplication.isPlaying)throw new InvalidOperationException("Stop Play Mode before building.");
        string output=Path.Combine(Repo,"Builds/BTL-Internal-0.4.0-Windows");Directory.CreateDirectory(output);
        var report=BuildPipeline.BuildPlayer(new BuildPlayerOptions
        {
            scenes=new[]{Root+"Main.unity"},locationPathName=Path.Combine(output,"BTL.exe"),
            target=BuildTarget.StandaloneWindows64,options=BuildOptions.None
        });
        if(report.summary.result!=BuildResult.Succeeded)throw new Exception("BTL Windows build: "+report.summary.result);
        File.Copy(Root+"Fonts/LICENSE.txt",Path.Combine(output,"FONT-LICENSE.txt"),true);
        File.WriteAllText(Path.Combine(output,"开始试玩.txt"),
            "字里行间 · 货场调查 · 标题下面的人\n内部离线试玩 0.4.0\n\n双击 BTL.exe。整个文件夹须一起保留。\n"+
            "采访：选表达卡 → 核对采访意图 → 确认或返回改写。可展开编辑原句；只有预写原句可以执行。\n"+
            "标题：选写法 → 复核所有含义 → 独立签发；也可暂缓。\n"+
            "材料册可随时翻阅，正文可选择复制；顶栏可调字号。输入框 Enter 换行，Tab 切换焦点。\n"+
            "只有当前一局；关闭或重开不保存。没有模型请求、联网账号或付费服务。\n\n"+
            "中文字体：Noto Sans CJK SC，SIL OFL 1.1，许可证随包附带。\n"+
            "静态像素画面由项目自有生成脚本绘制。\n");
        Debug.Log("BTL WINDOWS BUILD SUCCEEDED: "+output+"; bytes="+report.summary.totalSize);
    }
}
