# 初始化文件
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
import os
from app.config import Config

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
cors = CORS()

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY='dev',
            SQLALCHEMY_DATABASE_URI='sqlite:///health.db',
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.update(test_config)

    # 确保实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    # 注册蓝图
    from app.api import auth_api, health_record_api, recommendation_api, data_collection_api, federated_learning_api
    app.register_blueprint(auth_api.bp)
    app.register_blueprint(health_record_api.bp)
    app.register_blueprint(recommendation_api.bp)
    app.register_blueprint(data_collection_api.bp)
    app.register_blueprint(federated_learning_api.bp)

    # 在应用上下文中创建所有数据库表
    with app.app_context():
        try:
            # 导入所有模型以确保它们被注册
            from app.models import User, HealthRecord
            
            # 删除现有的数据库文件（如果存在）
            db_path = os.path.join(os.path.dirname(app.instance_path), 'health.db')
            if os.path.exists(db_path):
                os.remove(db_path)
            
            # 创建所有表
            db.create_all()
            print("成功创建数据库表")
            
            # 检查测试用户是否已存在
            test_user = User.query.filter_by(email='test@test.com').first()
            if not test_user:
                # 添加测试用户
                test_user = User(
                    username='test_user',
                    email='test@test.com'
                )
                test_user.set_password('test123')
                db.session.add(test_user)
                db.session.commit()
                print("成功创建测试用户")
            else:
                print("测试用户已存在")
            
        except Exception as e:
            print(f"初始化数据库时出错: {str(e)}")
            db.session.rollback()
            raise e

    return app 