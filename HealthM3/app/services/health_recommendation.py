# 健康推荐服务
from datetime import datetime, timedelta
import numpy as np

class HealthRecommendationService:
    def __init__(self):
        # 定义健康指标的正常范围
        self.normal_ranges = {
            'heart_rate': (60, 100),  # 每分钟心跳次数
            'blood_sugar': (3.9, 6.1),  # mmol/L
            'sleep_hours': (7, 9),  # 小时
            'mood_score': (7, 10),  # 1-10分
            'weight': (18.5, 24.9)  # BMI范围
        }

    def analyze_health_metrics(self, health_record):
        """分析健康指标，返回每个指标的状态评估"""
        analysis = {}
        
        # 分析心率
        heart_rate = health_record.heart_rate
        analysis['heart_rate'] = {
            'value': heart_rate,
            'status': self._get_status(heart_rate, self.normal_ranges['heart_rate']),
            'description': self._get_heart_rate_description(heart_rate)
        }
        
        # 分析血压
        try:
            systolic, diastolic = map(int, health_record.blood_pressure.split('/'))
            blood_pressure_status = self._analyze_blood_pressure(systolic, diastolic)
            analysis['blood_pressure'] = {
                'value': health_record.blood_pressure,
                'status': blood_pressure_status,
                'description': self._get_blood_pressure_description(systolic, diastolic)
            }
        except:
            analysis['blood_pressure'] = {
                'value': health_record.blood_pressure,
                'status': 'unknown',
                'description': '血压数据格式错误'
            }
        
        # 分析血糖
        blood_sugar = health_record.blood_sugar
        analysis['blood_sugar'] = {
            'value': blood_sugar,
            'status': self._get_status(blood_sugar, self.normal_ranges['blood_sugar']),
            'description': self._get_blood_sugar_description(blood_sugar)
        }
        
        # 分析睡眠时间
        sleep_hours = health_record.sleep_hours
        analysis['sleep_hours'] = {
            'value': sleep_hours,
            'status': self._get_status(sleep_hours, self.normal_ranges['sleep_hours']),
            'description': self._get_sleep_description(sleep_hours)
        }
        
        # 分析心情评分
        mood_score = health_record.mood_score
        analysis['mood_score'] = {
            'value': mood_score,
            'status': self._get_status(mood_score, self.normal_ranges['mood_score']),
            'description': self._get_mood_description(mood_score)
        }
        
        # 分析体重（BMI）
        weight = health_record.weight
        analysis['weight'] = {
            'value': weight,
            'status': self._get_status(weight, self.normal_ranges['weight']),
            'description': self._get_weight_description(weight)
        }
        
        return analysis

    def generate_recommendations(self, analysis):
        """基于健康指标分析生成个性化建议"""
        recommendations = []
        
        # 根据各项指标状态生成建议
        for metric, data in analysis.items():
            if data['status'] == 'low':
                recommendations.extend(self._get_low_recommendations(metric))
            elif data['status'] == 'high':
                recommendations.extend(self._get_high_recommendations(metric))
        
        # 如果所有指标正常，添加保持建议
        if not recommendations:
            recommendations.append("您的各项健康指标都在正常范围内，请继续保持当前的健康生活方式！")
        
        return recommendations

    def _get_status(self, value, normal_range):
        """判断指标值的状态（低、正常、高）"""
        if value < normal_range[0]:
            return 'low'
        elif value > normal_range[1]:
            return 'high'
        return 'normal'

    def _analyze_blood_pressure(self, systolic, diastolic):
        """分析血压状态"""
        if systolic < 90 or diastolic < 60:
            return 'low'
        elif systolic > 140 or diastolic > 90:
            return 'high'
        return 'normal'

    # 各项指标的描述生成方法
    def _get_heart_rate_description(self, value):
        if value < self.normal_ranges['heart_rate'][0]:
            return "心率偏低，可能感觉疲劳或头晕"
        elif value > self.normal_ranges['heart_rate'][1]:
            return "心率偏高，可能感觉心跳加快或焦虑"
        return "心率正常，心脏功能良好"

    def _get_blood_pressure_description(self, systolic, diastolic):
        if systolic < 90 or diastolic < 60:
            return "血压偏低，可能感觉头晕或疲劳"
        elif systolic > 140 or diastolic > 90:
            return "血压偏高，需要注意控制"
        return "血压正常，循环系统功能良好"

    def _get_blood_sugar_description(self, value):
        if value < self.normal_ranges['blood_sugar'][0]:
            return "血糖偏低，可能感觉饥饿或头晕"
        elif value > self.normal_ranges['blood_sugar'][1]:
            return "血糖偏高，需要注意控制"
        return "血糖正常，代谢功能良好"

    def _get_sleep_description(self, value):
        if value < self.normal_ranges['sleep_hours'][0]:
            return "睡眠时间不足，可能影响日间表现"
        elif value > self.normal_ranges['sleep_hours'][1]:
            return "睡眠时间过长，可能影响身体状态"
        return "睡眠时间适中，有助于身体恢复"

    def _get_mood_description(self, value):
        if value < self.normal_ranges['mood_score'][0]:
            return "心情状态欠佳，需要适当调节"
        return "心情状态良好，请继续保持"

    def _get_weight_description(self, value):
        if value < self.normal_ranges['weight'][0]:
            return "体重偏低，需要适当增加营养摄入"
        elif value > self.normal_ranges['weight'][1]:
            return "体重偏高，需要注意控制"
        return "体重正常，身体状态良好"

    # 针对异常指标的建议生成方法
    def _get_low_recommendations(self, metric):
        recommendations = {
            'heart_rate': [
                "适当进行有氧运动，如散步、慢跑等",
                "保持充足的休息和睡眠",
                "如果经常感觉头晕或疲劳，建议咨询医生"
            ],
            'blood_pressure': [
                "适当增加盐分摄入",
                "保持充足的水分补充",
                "避免突然起立或剧烈运动"
            ],
            'blood_sugar': [
                "规律进食，避免长时间空腹",
                "随身携带含糖食物以应对低血糖",
                "注意营养均衡，适量增加碳水化合物摄入"
            ],
            'sleep_hours': [
                "保持规律的作息时间",
                "创造良好的睡眠环境",
                "避免睡前使用电子设备"
            ],
            'mood_score': [
                "尝试进行放松活动，如瑜伽或冥想",
                "与亲朋好友多交流",
                "适当参加户外活动，增加阳光接触"
            ],
            'weight': [
                "适当增加饮食量",
                "增加优质蛋白质的摄入",
                "进行适度的力量训练"
            ]
        }
        return recommendations.get(metric, ["请咨询专业医生获取更详细的建议"])

    def _get_high_recommendations(self, metric):
        recommendations = {
            'heart_rate': [
                "避免剧烈运动和情绪激动",
                "学习放松技巧，如深呼吸",
                "减少咖啡因的摄入"
            ],
            'blood_pressure': [
                "限制盐分摄入",
                "保持规律运动",
                "避免压力和情绪波动"
            ],
            'blood_sugar': [
                "控制碳水化合物的摄入",
                "增加运动量",
                "规律监测血糖水平"
            ],
            'sleep_hours': [
                "适当增加日间活动量",
                "避免日间过长的午睡",
                "保持规律的作息时间"
            ],
            'weight': [
                "控制饮食摄入量",
                "增加运动频率",
                "选择低热量、高营养的食物"
            ]
        }
        return recommendations.get(metric, ["请咨询专业医生获取更详细的建议"]) 