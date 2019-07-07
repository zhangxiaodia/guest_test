#utf-8
from django.test import TestCase
from datetime import datetime
from sign.models import Event,Guest
from django.contrib.auth.models import User
# Create your tests here.
class ModelTest(TestCase):
	def setUp(self):
		Event.objects.create(id=3,name="one plus发布会",limit=10,status=True,address="深圳",start_time=datetime(2019,7,7,12,0,0))
		Guest.objects.create(realname="anna",phone=13000000000,mail="zhangxiaodi@qq.com",sign=False,event_id=1)
		
	def tearDown(self):
		pass
	def test_event_models(self):
		result=Event.objects.get(name="one plus发布会")
		self.assertEqual(result.address,"深圳")
		self.assertTrue(result.status)
	def test_guest_models(self):
		result=Guest.objects.get(realname="anna")
		self.assertEqual(result.phone,"13000000000")
		self.assertFalse(result.sign)

class IndexPageTest(TestCase):
	def test_index_page_renders_index_template(self):
		response=self.client.get("/index/")
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'index.html')

class LoginActionTest(TestCase):
	def setUp(self):
		User.objects.create_user("admin1","admin@admin.com","admin123")
	def tearDown(self):
		pass
	def test_add_admin(self):
		user=User.objects.get(username="admin1")
		self.assertEqual(user.username,'admin1')
		self.assertEqual(user.email,'admin@admin.com')
	def test_login_action_username_password_null(self):
		test_data={'username':'','password':''}
		response=self.client.post('/login_action/',data=test_data)
		self.assertEqual(response.status_code,200)
		self.assertIn(b"username or password error",response.content)
	def test_login_action_username_password_error(self):
		test_data={'username':'admin','password':'admin'}
		response=self.client.post('/login_action/',data=test_data)
		self.assertEqual(response.status_code,200)
		self.assertIn(b"username or password error",response.content)
	def test_login_action_username_password_success(self):
		test_data={'username':'admin1','password':'admin123'}
		response=self.client.post('/login_action/',data=test_data)
		self.assertEqual(response.status_code,302)

class EventManageTest(TestCase):
	def setUp(self):
		User.objects.create_user("admin1","admin@admin.com","admin123")
		Event.objects.create(id=3,name="one plus发布会",limit=10,status=True,address="sz",start_time=datetime(2019,7,7,12,0,0))
		self.login_user={'username':'admin1','password':'admin123'}
	def test_event_manage_success(self):
		response=self.client.post('/login_action/',data=self.login_user)
		response=self.client.post('/event_manage/')
		self.assertEqual(response.status_code,200)
#		self.assertIn(b'one plus发布会',response.content)
	def test_event_manage_search_success(self):
		response=self.client.post('/login_action/',data=self.login_user)
		response=self.client.post('/search_name/',{"name":"one plus发布会"})
		self.assertEqual(response.status_code,200)
#		self.assertIn(b"深圳",response.content)
		self.assertIn(b"sz",response.content)

class GuestManageTest(TestCase):
	def setUp(self):
		User.objects.create_user("admin1","admin@admin.com","admin123")
		Guest.objects.create(realname="anna",phone=13000000000,mail="zhangxiaodi@qq.com",sign=False,event_id=1)
		self.login_user={'username':'admin1','password':'admin123'}
	def test_event_manage_success(self):
		response=self.client.post('/login_action/',data=self.login_user)
		response=self.client.post('/guest_manage/')
		self.assertEqual(response.status_code,200)
		self.assertIn(b'zhangxiaodi@qq.com',response.content)
	def test_event_manage_search_success(self):
		response=self.client.post('/login_action/',data=self.login_user)
		response=self.client.post('/search_realname/',{"realname":"anna"})
		self.assertEqual(response.status_code,200)
#		self.assertIn(b"深圳",response.content)
		self.assertIn(b"anna",response.content)
