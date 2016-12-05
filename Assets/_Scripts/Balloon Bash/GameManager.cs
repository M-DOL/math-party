using UnityEngine;
using System.Collections;
using UnityEngine.UI;
using System.Collections.Generic;
using System.Linq;
using Assets._Scripts.Utils;

public class GameManager : MonoBehaviour {
    public GameObject dartPrefab, balloonPrefab;
    public Transform ballTrans;
    public List<GameObject> balloons;
    public List<Color> colors = new List<Color>();
    public int[] eqArr = new int[3];
    public string[] eqStringArr = new string[3];
    public Text eq;
    public AudioSource sound;
    private int first, second, sum, choice;
    private List<int> numbers;
    private Vector2[] locs = new Vector2[5];
    // Use this for initialization
    void Start ()
    {
        numbers = Enumerable.Range(0, 10).ToList();
        for (int i = 0; i < 5; ++i)
        {
            locs[i] = balloons[i].transform.position;
        }
        //Sets up question
        NewQuestion();
    }
	
	// Update is called once per frame
	void Update ()
    {

	}
    IEnumerator Request()
    {
        string url = "";
        WWW post = new WWW(url);
        yield return post;
    }
    void NewQuestion()
    {
        //Generate equation
        eqArr[0] = Random.Range(0, 9);
        while(eqArr[2] < eqArr[0])
        {
            eqArr[2] = Random.Range(0, 9);
        }
        eqArr[1] = eqArr[2] - eqArr[0];
        choice = Random.Range(0, 2);
        int answer = 0;
        for (int i = 0; i < 3; ++i)
        {
            if (choice == i)
            {
                answer = eqArr[i];
                eqStringArr[i] = "?";
            }
            else
            {
                eqStringArr[i] = eqArr[i].ToString();
            }
        }
        eq.text = System.String.Format("{0} + {1} = {2}", eqStringArr[0], eqStringArr[1], eqStringArr[2]);
        numbers.Remove(answer);
        numbers.Shuffle();
        //Set balloon colors
        int correctInd = Random.Range(0, 4);
        for (int i = 0; i < balloons.Count; ++i)
        {
            var balloon = balloons[i];
            balloon.GetComponent<Image>().color = colors[Random.Range(0, colors.Count - 1)];
            balloon.transform.GetChild(0).GetComponent<Text>().text = (correctInd == i) ? answer.ToString() : numbers[i].ToString();
            if(correctInd == i)
            {
                balloon.GetComponent<Balloon>().correct = true;
            }
        }
        numbers.Add(answer);
    }
    public void PlaySound(string name)
    {
        sound.PlayOneShot(Resources.Load(name) as AudioClip);
    }
    public void Fail()
    {
        PlaySound("Incorrect");
        eq.text = System.String.Format("{0} + {1} = {2}", eqArr[0], eqArr[1], eqArr[2]);
        eq.color = Color.red;
        StartCoroutine(PopAll());
    }
    IEnumerator PopAll()
    {
        foreach(GameObject balloon in balloons)
        {
            if(balloon != null)
            {
                PlaySound("Pop");
                Destroy(balloon);
                yield return new WaitForSeconds(.5f);
            }
        }
        for(int i = 0; i < balloons.Count; ++i)
        {
            GameObject ball = Instantiate(balloonPrefab, locs[i], Quaternion.identity) as GameObject;
            ball.transform.SetParent(ballTrans);
            balloons[i] = ball;
        }
        eq.color = Color.black;
        NewQuestion();
    }
    public void Success()
    {
        eq.color = Color.green;
        foreach(GameObject balloon in balloons)
        {
            Vector2 dir = (eq.transform.position - balloon.GetComponent<Text>().transform.position).normalized;
        }
    }
}
