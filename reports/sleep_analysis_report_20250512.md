
# Analiza Calității Somnului în Medii Dificile
**Data Raportului:** 12 May 2025

## Rezumat Executiv

Acest raport prezintă analiza a **1022 participanți** pentru a înțelege factorii care influențează calitatea somnului în medii dificile. Am identificat corelații semnificative între factorii de mediu și calitatea somnului, folosind modele de machine learning pentru predicție.

### Concluzii Principale:

1. **Factorii de mediu au un impact semnificativ negativ** asupra calității somnului
2. **Zgomotul este cel mai perturbator factor** (corelație: -0.41)
3. **Modelul AI poate prezice calitatea somnului** cu o acuratețe de 64%

## 1. Distribuția Calității Somnului

![Distribuția Calității Somnului](sleep_quality_distribution.png)

**Observații:**
- 63% din participanți raportează somn "Destul de Bun"
- 18% raportează somn "Foarte Bun"
- 19% au probleme cu somnul ("Destul de Rău" sau "Foarte Rău")

## 2. Factorii Principali care Influențează Somnul

![Feature Importance](feature_importance.png)

### Top 5 Factori (în ordinea importanței):

1. **Latența Somnului** (16.8%) - Timpul necesar pentru a adormi
2. **Durata Somnului** (15.3%) - Numărul de ore dormite
3. **Ora de Culcare** (11.4%) - Momentul când persoana se culcă
4. **Orele de Antrenament Militar** (10.3%)
5. **Frigul Nocturn** (8.4%)

## 3. Impactul Factorilor de Mediu

![Environmental Impact](environmental_impact.png)

### Corelații Factori de Mediu - Calitatea Somnului:

| Factor de Mediu | Corelație | Interpretare |
|----------------|-----------|--------------|
| Zgomot Nocturn | -0.414 | Impact negativ foarte mare |
| Frig Nocturn | -0.369 | Impact negativ mare |
| Tuse/Sforăit | -0.361 | Impact negativ mare |
| Căldură Nocturnă | -0.269 | Impact negativ moderat |

![Environmental Correlations](environmental_correlations_heatmap.png)

**Concluzii:**
- Toți factorii de mediu au impact negativ asupra somnului
- Zgomotul este cel mai perturbator factor
- Există corelații între diferiți factori de mediu

## 4. Pattern-uri de Somn

![Sleep Patterns](sleep_patterns_analysis.png)

### Corelații Cheie:
- **Durata Somnului vs Calitate**: +0.329 (corelație pozitivă moderată)
- **Latența Somnului vs Calitate**: -0.265 (corelație negativă)

**Interpretare:**
- Mai multe ore de somn = calitate mai bună
- Timp mai lung pentru a adormi = calitate mai slabă

## 5. Performanța Modelului AI

![Confusion Matrix](confusion_matrix_random_forest_classification.png)

### Rezultate Model:
- **Acuratețe Generală**: 63.9%
- **Cel Mai Bun la Prezicerea**: Somn "Destul de Bun" (85% recall)
- **Provocări**: Categoriile extreme (Foarte Rău/Foarte Bun)

## 6. Recomandări

### Pentru Îmbunătățirea Calității Somnului:

1. **Controlul Zgomotului**
   - Implementați măsuri de izolare fonică
   - Folosiți dopuri de urechi sau zgomot alb

2. **Managementul Temperaturii**
   - Mențineți temperatura camerei între 18-22°C
   - Asigurați ventilație adecvată

3. **Optimizarea Rutinei de Somn**
   - Ora constantă de culcare
   - Reducerea timpului de adormire prin tehnici de relaxare

4. **Monitorizare Continuă**
   - Folosiți modelul AI pentru predicții personalizate
   - Ajustați condițiile bazat pe feedback

## 7. Limitări și Cercetări Viitoare

- Datele sunt auto-raportate (posibil bias subiectiv)
- Studiu transversal (nu longitudinal)
- Recomandăm monitorizare obiectivă cu dispozitive

## Anexe

### Date Tehnice:
- Total participanți: 1022
- Features analizate: 11
- Algoritm folosit: Random Forest Classification
- Perioada colectării datelor: Mai 2022

---
*Raport generat automat folosind Python și Machine Learning*
