#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Servo.h>
WiFiClient client;

Servo myMotor;

const uint16_t port = 2222;
const char *host = "10.42.0.1";

const int n = 6;
int m[n] = {5, 4, 2, 12, 0, 15};

const int enc_l_pin = 14;          // Motor L
const int enc_r_pin = 13; 

volatile unsigned long enc_l = 0;
volatile unsigned long enc_r = 0;

int pwml;
int pwmr;

byte altCount = 0;

const int len = 11;
char a[len];

int cti(char c)
{
    return (int(c) - 48);
}

int sti(int s)
{
    int n = 0;
    for(int i = s; i < s + 3; i++)
    {
        n *= 10;
        n += cti(a[i]);
    }
    return n;
}
void setup()
{
    myMotor.attach(1);
    myMotor.write(35);
    
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
    for(int i = 0; i < n; i++)
        pinMode(m[i], OUTPUT);
        
    pinMode(enc_l_pin, INPUT_PULLUP);
    pinMode(enc_r_pin, INPUT_PULLUP);
    
    for(int i = 0; i < n; i++)
      digitalWrite(m[i], LOW);

//    Serial.begin(9600);
//    Serial.println("Connecting...\n");
      WiFi.mode(WIFI_STA);
      WiFi.begin("WIFI", "123456789"); 
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(200);
//        Serial.print(" .");
    }
//    Serial.println("Wifi Connected !!");
    digitalWrite(LED_BUILTIN, HIGH);

    attachInterrupt(digitalPinToInterrupt(enc_l_pin), countLeft, CHANGE);
    attachInterrupt(digitalPinToInterrupt(enc_r_pin), countRight, CHANGE);

}

void loop()
{
 
    if (!client.connect(host, port))
    {
//        Serial.println("Connection to host failed");
        return;
    }
 
    
    delay(40);
    for(int i = 0; client.available() > 0; i++)
    {
        a[i] = client.read();
//        Serial.print(a[i]);
    } 
//    Serial.println();
    
    if (a[10] == '1')
    {
      myMotor.write(130);
    }
    if (a[10] == '0')
    {
      myMotor.write(35);
    }
    for(int i = 0; i < 4; i++)
    {
      digitalWrite(m[i], cti(a[i]));
//      Serial.println(cti(a[i]));
    }
    pwml = sti(4);
    pwmr = sti(7);

    if (sti(0) == 101 || sti(0) == 010 )
    {
      pid();
    }
    
    analogWrite (m[4], pwml*4);
//    Serial.println(pwml*4);
    analogWrite (m[5], pwmr*4);
//    Serial.println(pwmr*4);
//    Serial.println();
    client.stop();
    
}

void pid()
{
  enc_l = 0;
  enc_r = 0;

  unsigned long enc_l_prev = enc_l;
  unsigned long enc_r_prev = enc_r;
  unsigned long diff_l;
  unsigned long diff_r;

  delay(50);

  diff_l = enc_l - enc_l_prev;
  diff_r = enc_r - enc_r_prev;
  int diff = diff_l - diff_r;
//  Serial.println(diff);

  if (altCount % 2 == 0)
  {
    if (diff_l > diff_r)
    {
      pwmr += diff/2;
    }
    
    if (diff_l < diff_r)
    {
      pwmr -= diff/2;
    }
  }

  else
  {
    if (diff_l > diff_r)
    {
      pwml -= diff;
    }
    
    if (diff_l < diff_r)
    {
      pwml += diff;
    }
  }
 
//  Serial.println(diff_l);
//  Serial.println(diff_r);
//  Serial.println();    
}
void countLeft() {
  enc_l++;
  }

void countRight() {
  enc_r++;  
}
