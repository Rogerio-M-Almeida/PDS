int led_male = 8;    // Pino para LED masculino
int led_female = 9;  // Pino para LED feminino
int led_unknown = 10; // Pino para LED indefinido

void setup() {
  pinMode(led_male, OUTPUT);
  pinMode(led_female, OUTPUT);
  pinMode(led_unknown, OUTPUT);
  
  Serial.begin(9600);  // Inicializa a comunicação serial
  while (!Serial) {    // Aguarda a inicialização da comunicação
    ; // Faz nada, só aguarda
  }
}

void loop() {
  if (Serial.available() > 0) {
    char gender_signal = Serial.read();
    
    // Apaga todos os LEDs
    digitalWrite(led_male, LOW);
    digitalWrite(led_female, LOW);
    digitalWrite(led_unknown, LOW);
    
    // Acende o LED correspondente
    if (gender_signal == '1') {
      digitalWrite(led_male, HIGH);   // Voz masculina
      Serial.println("Masculino");
    } else if (gender_signal == '2') {
      digitalWrite(led_female, HIGH); // Voz feminina
      Serial.println("Feminino");
    } else if (gender_signal == '3') {
      digitalWrite(led_unknown, HIGH);// Indefinido
      Serial.println("Indefinido");
    }
  }
}

