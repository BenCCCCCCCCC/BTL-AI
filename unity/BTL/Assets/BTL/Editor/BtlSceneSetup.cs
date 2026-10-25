using System.IO;
using BTL;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.UIElements;

public static class BtlSceneSetup
{
    const string ScenePath = "Assets/BTL/Main.unity";
    const string PanelPath = "Assets/BTL/MainPanel.asset";
    const string ContentPath = "Assets/BTL/Content/Generated/railyard_chapter.v1.0.json";

    [MenuItem("BTL/Build U2 Main")]
    public static void Build()
    {
        if (File.Exists(ScenePath))
        { Debug.Log("BTL Main already exists; preserving it."); return; }
        var source = AssetDatabase.LoadAssetAtPath<TextAsset>(ContentPath);
        if (source == null) throw new System.InvalidOperationException("Chapter JSON missing: " + ContentPath);
        var panel = AssetDatabase.LoadAssetAtPath<PanelSettings>(PanelPath);
        if (panel == null)
        {
            panel = ScriptableObject.CreateInstance<PanelSettings>();
            AssetDatabase.CreateAsset(panel, PanelPath);
            AssetDatabase.SaveAssets();
        }
        var scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
        var go = new GameObject("BTL Chapter UI");
        var document = go.AddComponent<UIDocument>(); document.panelSettings = panel;
        var view = go.AddComponent<ChapterUI>(); view.chapter = source;
        EditorSceneManager.SaveScene(scene, ScenePath);
        EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(ScenePath,true) };
        AssetDatabase.SaveAssets();
        Debug.Log("BTL U2 Main ready: " + ScenePath);
    }
}
