﻿using UnityEngine;
using System.Collections;
using UnityEngine.UI;
using System.Collections.Generic;
using System.Linq;
using Assets._Scripts.Utils;
using UnityEngine.Networking;
public class GameManager : MonoBehaviour
{
    public static GameManager S;
    public int correctThres = 7;
    public GameObject dartPrefab, balloonPrefab;
    public Transform ballTrans;
    public List<GameObject> balloons;
    public List<Color> colors = new List<Color>();
    public int[] eqArr = new int[3];
    public string[] eqStringArr = new string[3];
    public Text eq;
    public AudioSource sound;
    public float textSpeed = 1f;
    private float startTime;
    private int choice, correctInd;
    private List<int> numbers;
    private Vector2[] locs = new Vector2[5];
    private int correct = 0, level = 0;
    private string playerName = "";
    public Image currEnvironment;
    public InputField nameIn;
    public GameObject startPanel;
    public Sprite[] environments;
    private bool add;
    public bool running = false;
    void Awake()
    {
        S = this;
    }
    // Use this for initialization
    void Start()
    {
        numbers = Enumerable.Range(0, 10).ToList();
    }
    public void StartGame()
    {
        sound.Play();
        running = true;
        playerName = nameIn.text;
        Destroy(startPanel);
        StartCoroutine(FirstRequest(playerName));
        for (int i = 0; i < 5; ++i)
        {
            locs[i] = balloons[i].transform.position;
        }
        //Sets up question
        NewQuestion();
    }
    IEnumerator FirstRequest(string name)
    {
        string json = "{\"name\":\"" + name + "\"}";
        string local_url = "http://localhost:5000/api/api_new_student", hosted_url = "https://math-party.herokuapp.com/api/api_new_student";
        UnityWebRequest local_req = UnityWebRequest.Post(local_url, json);
        local_req.SetRequestHeader("Content-Type", "application/json");
        yield return local_req.Send();
        UnityWebRequest hosted_req = UnityWebRequest.Post(hosted_url, json);
        hosted_req.SetRequestHeader("Content-Type", "application/json");
        yield return hosted_req.Send();
    }
    IEnumerator UpdateDB(string name, bool result, float time)
    {
        string json = "{\"name\":\"" + name + "\",\"result\":" + (result ? 1: 0) + ",\"time\":" + time + "}";
        string local_url = "http://localhost:5000/api/api_class", hosted_url = "https://math-party.herokuapp.com/api/api_class";
        UnityWebRequest local_req = UnityWebRequest.Post(local_url, json);
        local_req.SetRequestHeader("Content-Type", "application/json");
        yield return local_req.Send();
        UnityWebRequest hosted_req = UnityWebRequest.Post(hosted_url, json);
        hosted_req.SetRequestHeader("Content-Type", "application/json");
        yield return hosted_req.Send();
    }
    int GenQuestion()
    {
        add = (Random.value >= .5) || level == 0;
        int max = level == 2 ? 20 : 9;
        int min = level == 2 ? 10 : 1;
        eqArr[2] = Random.Range(min, max); ;
        eqArr[0] = Random.Range(min, eqArr[2]);
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
        eq.text = add ? System.String.Format("{0} + {1} = {2}", eqStringArr[0], eqStringArr[1], eqStringArr[2])
        : System.String.Format("{0} - {1} = {2}", eqStringArr[2], eqStringArr[1], eqStringArr[0]);
        return answer;
    }
    void NewQuestion()
    {
        startTime = Time.time;
        //Generate equation
        int answer = GenQuestion();
        numbers.Remove(answer);
        numbers.Shuffle();
        //Set balloon colors
        correctInd = Random.Range(0, 4);
        for (int i = 0; i < balloons.Count; ++i)
        {
            var balloon = balloons[i];
            balloon.GetComponent<Image>().color = colors[Random.Range(0, colors.Count - 1)];
            balloon.transform.GetChild(0).GetComponent<Text>().text = (correctInd == i) ? answer.ToString() : numbers[i].ToString();
            if (correctInd == i)
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
        correct = 0;
        StartCoroutine(UpdateDB(playerName, false, Time.time - startTime));
        PlaySound("Incorrect");
        eq.text = add ? System.String.Format("{0} + {1} = {2}", eqArr[0], eqArr[1], eqArr[2])
        : System.String.Format("{0} - {1} = {2}", eqArr[2], eqArr[1], eqArr[0]);
        eq.color = Color.red;
        StartCoroutine(PopAll());
    }
    IEnumerator PopAll()
    {
        foreach (GameObject balloon in balloons)
        {
            if (balloon != null)
            {
                PlaySound("Pop");
                Destroy(balloon);
                yield return new WaitForSeconds(.5f);
            }
        }
        for (int i = 0; i < balloons.Count; ++i)
        {
            GameObject ball = Instantiate(balloonPrefab, locs[i], Quaternion.identity) as GameObject;
            ball.transform.SetParent(ballTrans);
            balloons[i] = ball;
        }
        eq.color = Color.black;
        NewQuestion();
        if (correct >= correctThres && level != 2)
        {
            NewLevel();
        }
    }
    public void NewLevel()
    {
        ++level;
        correct = 0;
        currEnvironment.sprite = environments[level];
    }
    public void Success()
    {
        ++correct;
        StartCoroutine(UpdateDB(playerName, true, Time.time - startTime));
        eq.color = Color.green;
        PlaySound("Success");
        Vector2 dir = Vector2.zero;
        Text text = balloons[correctInd].transform.GetChild(0).GetComponent<Text>();
        dir = (eq.transform.position - text.transform.position).normalized;
        StartCoroutine(Congratulate(dir, text));
    }
    IEnumerator Congratulate(Vector3 dir, Text text)
    {
        while (Vector3.Magnitude(eq.transform.position - text.transform.position) > 100f)
        {
            Vector3 newPos = text.transform.position + dir * textSpeed;
            text.transform.position = newPos;
            yield return new WaitForSeconds(.03f);
        }
        Destroy(text.transform.gameObject);
        eq.text = add ? System.String.Format("{0} + {1} = {2}", eqArr[0], eqArr[1], eqArr[2]) :
            System.String.Format("{0} - {1} = {2}", eqArr[2], eqArr[1], eqArr[0]); ;
        StartCoroutine(PopAll());
    }
}
