#include <ESP8266WiFi.h>
#include <WiFiClient.h>

const uint16_t port = 1234;
const char *host = "192.168.137.1";
WiFiClient client;

int n = 6;
  int h = 100;
int m[6] = {14,12,15,13,2,0};
void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
    for(int i = 0; i < n; i++)
        pinMode(m[i], OUTPUT);

    digitalWrite(LED_BUILTIN, LOW);
    for(int i = 0; i < n; i++)
      digitalWrite(m[i], LOW);

    Serial.begin(115200);
    Serial.println("Connecting...\n");
    WiFi.mode(WIFI_STA);
    WiFi.begin("WIFI", "123456789"); 
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(" .");
    }
    Serial.println("Wifi Connected !!");
    digitalWrite(LED_BUILTIN, h);
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
    string s = "";
    while (client.available() > 0)
    {
        char c = client.read();
        s += c;
    }
    serial.println(s);
    client.stop();
}
