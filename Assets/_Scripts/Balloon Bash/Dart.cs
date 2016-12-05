using UnityEngine;
using System.Collections;

public class Dart : MonoBehaviour {
    public GameObject dartPrefab;
    public float vertSpeed = 1f, horSpeed = 1f, leftBound = 100f, rightBound = 700f, timeDur = 4f, start, yStart;
    bool flying = false;
    GameManager manage;
    public Canvas canvas;
    // Use this for initialization
    void Awake()
    {
        manage = Camera.main.GetComponent<GameManager>();
        yStart = transform.position.y;
    }
    void Update()
    {
        if(Input.GetKeyDown(KeyCode.Space))
        {
            flying = true;
            start = Time.time;
            manage.PlaySound("Throw");
        }
        Vector2 newPos = transform.position;
        if (flying)
        {
            newPos.y += vertSpeed;
            if(start + timeDur < Time.time)
            {
                MakeDart();
                Destroy(gameObject);
            }
        }
        else
        {
            newPos.x = Mathf.Clamp(newPos.x + horSpeed * Input.GetAxis("Horizontal"), 25f, 740f);
        }
        transform.position = newPos;
    }
	void OnCollisionEnter2D(Collision2D coll)
    {
        manage.PlaySound("Pop");
        MakeDart();
        Vector2 spawn = new Vector2(coll.transform.position.x, coll.transform.position.y);
        bool corr = coll.transform.GetComponent<Balloon>().correct, succ = coll.transform.parent.childCount == 2;
        Destroy(coll.transform.gameObject);
        Destroy(gameObject);
        if(corr)
        {
            //Failure
            manage.Fail();
        }
        else if(succ)
        {
            //Success
            manage.Success();
        }
    }
    void MakeDart()
    {
        GameObject dart = Instantiate(dartPrefab, new Vector2(transform.position.x, yStart), Quaternion.identity) as GameObject;
        dart.transform.SetParent(canvas.transform);
    }
}
