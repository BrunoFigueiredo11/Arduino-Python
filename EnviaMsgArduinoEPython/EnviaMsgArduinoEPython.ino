int led = 13;
void setup() {
  Serial.begin(9600); // Inicia a comunicação serial com uma taxa de transmissão de 9600 bps
   pinMode(led,OUTPUT);
}

void loop() {
  if (Serial.available() > 0) { // Verifica se há dados disponíveis para leitura
    String valor = Serial.readString(); // Lê a mensagem enviada pelo Python
    if(valor == "1"){
       digitalWrite(led, HIGH); //acende (HIGH) o led
       Serial.println("1");
      }else if(valor == "0"){        
       digitalWrite(led, LOW); //acende (HIGH) o led
       Serial.println("0");
        }
  }
}
