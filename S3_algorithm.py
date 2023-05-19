class S3Orchestrator:
    def scorer(self, previews):
        scores = []
        for preview in previews:
            try:
                confidence = preview(E)
                scores.append(confidence)
            except:

                scores.append(0)
        return scores

    def selector(self, scores, threshold, k):
        selected = []
        for i, score in enumerate(scores):
            if score >= threshold and len(selected) < k:
                selected.append(i)
        return selected

    def sequencer(self, selected):
        sequence = []
        for index in selected:
            sequence.append(index)
        return sequence

    def Run_S3_Orchestrator(self, previews, threshold, k):
        scores = self.scorer(previews)
        selected = self.selector(scores, threshold, k)
        sequence = self.sequencer(selected)
        return scores, selected, sequence


