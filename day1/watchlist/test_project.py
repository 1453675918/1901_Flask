import unittest

from blog import app, db
from blog.models import Movies, User

class ProjectTestCase(unittest.TestCase):

    #测试固件
    def setUp(self):
        # 更新配置
        app.config.update(
            TESTING = True,
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        )

        db.create_all()
        user = User(name='Test', username='test')
        user.set_password('123456')
        movies = Movies(title='test movie title', year=2020)

        db.session.add_all([user,movies])
        db.session.commit()

        self.client = app.test_client() # 测试客户端
        self.runner = app.test_cli_runner() # 创建测试


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    
    # 测试app是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)

    # 程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])
    
    # 测试404页面
    def test_404_page(self):
        response = self.client.get('/lalala')
        data = response.get_data(as_text=True)
        self.assertIn('页面走丢了~~~ 404',data)
        self.assertIn('返回首页',data)
        self.assertEqual(response.status_code,404)
    
    # 测试主页
    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('test movie title',data)
        self.assertIn('Test',data)
        self.assertEqual(response.status_code,200)

if __name__ == "__main__":
    unittest.main()