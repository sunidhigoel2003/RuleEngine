from django.db import models

# Create your models here.


class Node(models.Model):
    NODE_TYPE_CHOICES = [('operator', 'Operator'), ('operand', 'Operand')]
    type = models.CharField(max_length=10, choices=NODE_TYPE_CHOICES)
    left = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='left_child')
    right = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='right_child')
    value = models.CharField(max_length=255, null=True, blank=True)

class Rule(models.Model):
    rule_string = models.TextField()
    root_node = models.ForeignKey(Node, on_delete=models.CASCADE)


