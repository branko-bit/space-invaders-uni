using UnityEngine;

public class BackgroundMovementScript : MonoBehaviour
{
    public float speed = 0.1f; // Speed of the background
    private float offset; // Offset of the background
    private Material mat; // Material of the background
    public float textureScale = 1.0f; // Scale of the texture


    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        mat = GetComponent<Renderer>().material;
        mat.SetTextureScale("_MainTex", new Vector2(textureScale, textureScale));
    }

    // Update is called once per frame
    void Update()
    {
        offset += speed * Time.deltaTime;
        mat.SetTextureOffset("_MainTex", new Vector2(0, offset));
    }
}
