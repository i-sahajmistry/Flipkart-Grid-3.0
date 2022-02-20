#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Servo.h>
WiFiClient client;

Servo myMotor;

const uint16_t port = 1111;
const char *host = "10.42.0.1";

const int n = 6;
int m[n] = {14,12,15,13,2,0};

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
    myMotor.attach(4);
    myMotor.write(0);
    
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
    for(int i = 0; i < n; i++)
        pinMode(m[i], OUTPUT);

    for(int i = 0; i < n; i++)
      digitalWrite(m[i], LOW);

    Serial.begin(250000);
    Serial.println("Connecting...\n");
    WiFi.mode(WIFI_STA);
    WiFi.begin("WIFIA", "123456789"); 
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(200);
        Serial.print(" .");
    }
    Serial.println("Wifi Connected !!");
    digitalWrite(LED_BUILTIN, HIGH);

}

void loop()
{
    Serial.println(1);
    if (!client.connect(host, port))
    {
        Serial.println("Connection to host failed");
        return;
    }
    Serial.println(2);
    
    delay(40);
    for(int i = 0; client.available() > 0; i++)
    {
        a[i] = client.read();
        Serial.print(a[i]);
    } 
    Serial.println();
    if (a[10] == '1')
    {
      myMotor.write(130);
    }
    if (a[10] == '0')
    {
      myMotor.write(0);
    }
    for(int i = 0; i < 4; i++)
    {
      digitalWrite(m[i], cti(a[i]));
      Serial.println(cti(a[i]));
    }
    analogWrite (m[4], sti(4));
    Serial.println(sti(4));
    analogWrite (m[5], sti(7));
    Serial.println(sti(7));
    Serial.println();
    client.stop();
    //delay(100);
}
