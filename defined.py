class Patient():
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.symptoms =[]
  # def Symptoms(self):
  #     return self.Symptoms     
        
    
def Add(patient,symptom):
    patient.symptoms.append(symptom)
    
def Len(patient):
    return len(patient.symptoms)    
       
def Find(patient,condition): # Detecta si un paciente contiene una enfermedad 
    conditions = patient.symptoms
    for c in conditions:
        if c==condition:
            return 1
    return 0
    
def BreastCancer(patient):
    if Find(patient,"bulto") or Find(patient,"secrecion") or Find(patient,"retraccion") or Find(patient,"descamacion") or Find(patient,"hundimiento") :
        return 1
    return 0    

def OvarianCancer(patient):
    if patient.age > 51 and Find(patient,"secrecion"): return 1
    if Find(patient,"dolor") or Find(patient,"bulto") or Find(patient,"hinchazon") or Find(patient,"orine") or Find(patient,"llenura") :
        return 1
    return 0    

def PancreaticCancer(patient):
    if Find(patient,"ictericia") or Find(patient,"perdida peso") or Find(patient,"dolor") or Find(patient,"esteatorrea") or Find(patient,"glucosa") :
        return 1
    return 0  
    
    
                
            
# class Condition():
#     def __init__(self,name,*symptoms):
#         self.name = name
#         self.symptoms = list(symptoms)
        
#     # def add(self,symptom):
#     #     self.symptoms.append(symptom)    
       
#--------Prueba-------------
p = Patient("Fernando",35)
print(p.symptoms)       