#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>

const uint16_t port = 1234;
const char *host = "10.42.0.1";
WiFiClient client;

int m = 0;
int _m = 2;

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(m, OUTPUT);
    pinMode(_m, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
    digitalWrite(m, LOW);
    digitalWrite(_m, LOW);
    Serial.begin(9600);
    Serial.println("Connecting...\n");
    WiFi.mode(WIFI_STA);
    WiFi.begin("Anthrax-Inspiron-5580", "x8XDXYnq"); 
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print("  .");
    }
    Serial.println("Wifi Connected !!");
    digitalWrite(LED_BUILTIN, HIGH);
}

void loop()
{
    if (!client.connect(host, port))
    {
        Serial.println("Connection to host failed");
        delay(1000);
        return;
    }
    //Serial.println("Connected to server successful!");
    //client.println("Hello From ESP8266");
    delay(250);
    while (client.available() > 0)
    {
        char c = client.read();
        if(c == 'H')
        {
          Serial.println(c);
          digitalWrite(_m, HIGH);
          digitalWrite(m, LOW);
          delay(7000);                   
        }
        else
        {
          Serial.println(c);
          digitalWrite(m, HIGH);
          digitalWrite(_m, LOW);
          delay(7000); 
        }
    }
    client.stop();
}
