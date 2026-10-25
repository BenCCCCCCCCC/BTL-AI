using System;
using MCPForUnity.Editor.Services;
using UnityEditor;
using UnityEngine;

// Editor-only environment setup. Does not create or modify gameplay objects.
public static class BtlMcpConnection
{
    [MenuItem("BTL/Connect Local MCP")]
    public static async void Connect()
    {
        try
        {
            var config = EditorConfigurationCache.Instance;
            config.SetUseHttpTransport(true);
            config.SetHttpTransportScope("local");
            config.SetHttpBaseUrl("http://127.0.0.1:8080");
            bool connected = await MCPServiceLocator.Bridge.StartAsync();
            if (connected)
                Debug.Log("BTL environment: local MCP connected. Project: " + Application.dataPath);
            else
                Debug.LogError("BTL environment: MCP connection failed. Start the local server, then use BTL/Connect Local MCP.");
        }
        catch (Exception error)
        {
            Debug.LogException(error);
        }
    }
}
