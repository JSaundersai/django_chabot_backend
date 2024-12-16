from datetime import datetime

from rest_framework import serializers


class TranslationSerializer(serializers.Serializer):
    language = serializers.CharField()
    text = serializers.CharField()


# added new serializers for the chat conversation and history
class MessageSerializer(serializers.Serializer):
    role = serializers.CharField()
    content = serializers.CharField()
    timestamp = serializers.DateTimeField(default=datetime.now)


class ConversationMetadataSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    user_id = serializers.CharField()
    agent_id = serializers.CharField()
    admin_id = serializers.CharField()
    timestamp = serializers.DateTimeField(default=datetime.now)
    messages = MessageSerializer(many=True)
    translations = TranslationSerializer(many=True)


class UserInputSerializer(serializers.Serializer):
    prompt = serializers.CharField()
    user_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class PromptConversationSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True)
    conversation_id = serializers.CharField(required=True)
    user_id = serializers.CharField(required=True)


class MessageDataSerializer(serializers.Serializer):
    text = serializers.JSONField(required=True)  # For array or string
    sender = serializers.CharField()
    user = serializers.CharField()
    timestamp = serializers.DateTimeField()
    agent_id = serializers.CharField(required=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Map sender to role for test compatibility
        data["role"] = data.pop("sender")
        # Map text to content for test compatibility
        data["content"] = data.pop("text")
        return data

    def to_internal_value(self, data):
        try:
            text_data = data.get("text")
            # Clean up [object Object] artifacts if it's an array
            if isinstance(text_data, list):
                text_data = [
                    str(item).replace("[object Object]", "").strip()
                    for item in text_data
                    if item
                ]

            return {
                "text": text_data,
                "sender": data["sender"],
                "user": data.get("user", ""),
                "timestamp": data["timestamp"],
                "agent_id": data.get("agent_id", ""),
            }
        except Exception as e:
            raise serializers.ValidationError(f"Data validation failed: {str(e)}")


class CompleteConversationsSerializer(serializers.Serializer):
    conversation_id = serializers.CharField(required=True)
    messages = MessageDataSerializer(many=True, required=True)


class CaptureFeedbackSerializer(serializers.Serializer):
    conversation_id = serializers.CharField()
    user_input = serializers.CharField()
    ai_response = serializers.CharField()
    correct_bool = serializers.BooleanField()
    chat_rating = serializers.IntegerField()
    correct_answer = serializers.CharField(required=False, allow_blank=True)
    metadata = serializers.DictField(required=False)
