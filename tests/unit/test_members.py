from unittest import TestCase
from src.member import Member

class TestMember(TestCase):
    def setUp(self):
        self.member=Member(1,"Zim","male")
    
    def test_initilization(self):
        # Check instance
        self.assertEqual(isinstance(self.member, Member),True)
        # Check properties
        self.assertEqual(self.member.id,1)
        self.assertEqual(self.member.name,"Zim")
        self.assertEqual(self.member.gender,"male")
        self.assertEqual(self.member.mother,None)
        self.assertEqual(self.member.father,None)
        self.assertEqual(self.member.spouse,None)
        self.assertEqual(self.member.child,[])