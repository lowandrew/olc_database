from django.db import models


# Create your models here.
class Sample(models.Model):
    seqid = models.CharField(max_length=56)

    def __str__(self):
        return self.seqid


class SeqData(models.Model):
    seqid = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='seqdata')
    n50 = models.IntegerField()
    num_contigs = models.IntegerField()
    rmlst = models.CharField(max_length=56)
    date_sequenced = models.DateField()


class LSTSData(models.Model):
    seqid = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='lsts_data')
    lsts_id = models.CharField(max_length=88)
    country_of_origin = models.CharField(max_length=128)
    food = models.CharField(max_length=128)

    def __str__(self):
        return self.lsts_id
