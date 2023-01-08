class Patient():
    def __init__(self,name,sex,age):
        self.name = name
        self.sex  = sex
        self.age  = age
        self.symptoms =[]
  
    def add(self,symptom):
        return self.symptoms.append(symptom)

    def remove(self,symptom):
        return self.symptoms.remove(symptom)
    
    def len(self):
        return len(self.symptoms)    
       
def Find(patient,condition): # Detecta si un paciente contiene una enfermedad 
    conditions = patient.symptoms
    for c in conditions:
        if c==condition:
            return True
    return False
    
def BreastCancer(patient):
    if Find(patient,"bulto") or Find(patient,"secrecion") or Find(patient,"retraccion") or Find(patient,"descamacion") or Find(patient,"hundimiento") :
        return True
    return False    

def OvarianCancer(patient):
    if patient.age > 51 and Find(patient,"secrecion"): return 1
    if Find(patient,"dolor") or Find(patient,"bulto") or Find(patient,"hinchazon") or Find(patient,"orine") or Find(patient,"llenura") :
        return True
    return False    

def PancreaticCancer(patient):
    if Find(patient,"ictericia") or Find(patient,"perdida peso") or Find(patient,"dolor") or Find(patient,"esteatorrea") or Find(patient,"glucosa") :
        return True
    return False  
    


