using UnityEngine;
using System.Collections;

public class Balloon : MonoBehaviour {
    public float moveRange = .2f;
    public float offset;
    public bool correct = false;
	// Use this for initialization
	void Start ()
    {
        offset = Random.Range(0f, 10f);
    }
	
	// Update is called once per frame
	void FixedUpdate ()
    {
        Vector2 newPos = transform.position;
        newPos.x += Mathf.Sin(Time.fixedTime + offset) * moveRange;
        transform.position = newPos;
    }
}
