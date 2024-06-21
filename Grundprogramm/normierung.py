class Normierer:
    def __init__(self):
        self.messwerte = []
        self.mittelwert = 0
        self.spannweite = 0
        self.normierung_fertig = False

    def erfasse_messwert(self, wert):
        if not self.normierung_fertig:
            self.messwerte.append(wert)
            if len(self.messwerte) == 40:
                self.berechne_normierungsparameter()

    def berechne_normierungsparameter(self):
        self.mittelwert = sum(self.messwerte) / len(self.messwerte)
        self.spannweite = max(self.messwerte) - min(self.messwerte)
        self.normierung_fertig = True

    def normiere_wert(self, wert):
        if not self.normierung_fertig:
            self.erfasse_messwert(wert)
            return wert  # Unnormierter Wert während der Erfassungsphase

        # Normierung des Wertes
        normierter_wert = ((wert - self.mittelwert) / self.spannweite) * 200
        normierter_wert = normierter_wert / 10        


        # Bereichsbegrenzung
        if normierter_wert > 100:
            normierter_wert = 100
        elif normierter_wert < -100:
            normierter_wert = -100
        elif normierter_wert > -20 and normierter_wert < 20:
            normierter_wert = 0
        
        return int(normierter_wert)
