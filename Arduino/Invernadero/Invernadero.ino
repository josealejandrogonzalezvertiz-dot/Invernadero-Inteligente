
// Proyecto: Invernadero Inteligente
// Sistema de temperatura y riego automatico

#include <Arduino.h>

// Pines de los sensores
const int PIN_TEMPERATURA = 2;
const int PIN_HUMEDAD = A0;

// Pines de los actuadores
const int PIN_VENTILADOR = 7;
const int PIN_BOMBA = 8;

// Limites de temperatura
const float TEMP_MAXIMA = 30.0;
const float TEMP_MINIMA = 28.0;

// Limites de humedad del suelo
const int HUMEDAD_MINIMA = 40;
const int HUMEDAD_MAXIMA = 60;

void setup() {
  Serial.begin(9600);

  Serial.println("Invernadero Inteligente");
  Serial.println("Iniciando sistema...");
}

void loop() {
  // Modulo de temperatura y ventilacion

  // Modulo de humedad y riego

  delay(2000);
}
