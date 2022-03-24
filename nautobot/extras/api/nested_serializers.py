from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from nautobot.core.api import ChoiceField, ContentTypeField, WritableNestedSerializer
from nautobot.extras import choices, models
from nautobot.users.api.nested_serializers import NestedUserSerializer

__all__ = [
    "NestedConfigContextSerializer",
    "NestedConfigContextSchemaSerializer",
    "NestedCustomFieldSerializer",
    "NestedCustomLinkSerializer",
    "NestedDynamicGroupSerializer",
    "NestedExportTemplateSerializer",
    "NestedGitRepositorySerializer",
    "NestedGraphQLQuerySerializer",
    "NestedImageAttachmentSerializer",
    "NestedJobSerializer",
    "NestedJobLogEntrySerializer",
    "NestedJobResultSerializer",
    "NestedRelationshipSerializer",
    "NestedRelationshipAssociationSerializer",
    "NestedScheduledJobSerializer",
    "NestedSecretSerializer",
    "NestedSecretsGroupSerializer",
    "NestedStatusSerializer",
    "NestedTagSerializer",
    "NestedWebhookSerializer",
]


class NestedConfigContextSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:configcontext-detail")

    class Meta:
        model = models.ConfigContext
        fields = ["id", "url", "name"]


class NestedConfigContextSchemaSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:configcontextschema-detail")

    class Meta:
        model = models.ConfigContextSchema
        fields = ["id", "url", "name", "slug"]


class NestedCustomFieldSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:customfield-detail")

    class Meta:
        model = models.CustomField
        fields = ["id", "url", "name"]


class NestedCustomLinkSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:customlink-detail")
    content_type = ContentTypeField(
        queryset=ContentType.objects.all(),
    )

    class Meta:
        model = models.CustomLink
        fields = ["content_type", "id", "name", "url"]


class NestedDynamicGroupSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:dynamicgroup-detail")
    content_type = ContentTypeField(
        queryset=ContentType.objects.all(),
    )

    class Meta:
        model = models.DynamicGroup
        fields = ["id", "url", "name", "slug", "content_type"]


class NestedExportTemplateSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:exporttemplate-detail")

    class Meta:
        model = models.ExportTemplate
        fields = ["id", "url", "name"]


class NestedGitRepositorySerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:gitrepository-detail")

    class Meta:
        model = models.GitRepository
        fields = ["id", "url", "name"]


class NestedGraphQLQuerySerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:graphqlquery-detail")

    class Meta:
        model = models.GraphQLQuery
        fields = ["id", "url", "name"]


class NestedImageAttachmentSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:imageattachment-detail")

    class Meta:
        model = models.ImageAttachment
        fields = ["id", "url", "name", "image"]


class NestedJobSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:job-detail")

    class Meta:
        model = models.Job
        fields = ["id", "url", "source", "module_name", "job_class_name", "grouping", "name"]


class NestedJobLogEntrySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:joblogentry-detail")

    class Meta:
        model = models.JobLogEntry
        fields = [
            "id",
            "url",
            "absolute_url",
            "created",
            "grouping",
            "log_level",
            "log_object",
            "message",
        ]


class NestedJobResultSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:jobresult-detail")
    status = ChoiceField(choices=choices.JobResultStatusChoices)
    user = NestedUserSerializer(read_only=True)

    class Meta:
        model = models.JobResult
        fields = ["id", "url", "name", "created", "completed", "user", "status"]


class NestedRelationshipSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:relationship-detail")

    class Meta:
        model = models.Relationship
        fields = ["id", "url", "name", "slug"]


class NestedRelationshipAssociationSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:relationshipassociation-detail")

    class Meta:
        model = models.RelationshipAssociation
        fields = ["id", "url", "relationship", "source_id", "destination_id"]


class NestedScheduledJobSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False)
    start_time = serializers.DateTimeField(format=None, required=False)

    class Meta:
        model = models.ScheduledJob
        fields = ["name", "start_time", "interval"]

    def validate(self, data):
        data = super().validate(data)

        if data["interval"] != choices.JobExecutionType.TYPE_IMMEDIATELY:
            if "name" not in data:
                raise serializers.ValidationError({"name": "Please provide a name for the job schedule."})

            if "start_time" not in data or data["start_time"] < models.ScheduledJob.earliest_possible_time():
                raise serializers.ValidationError(
                    {
                        "start_time": "Please enter a valid date and time greater than or equal to the current date and time."
                    }
                )

        return data


class NestedSecretSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:secret-detail")

    class Meta:
        model = models.Secret
        fields = ["id", "url", "name", "slug"]


class NestedSecretsGroupSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:secretsgroup-detail")

    class Meta:
        model = models.SecretsGroup
        fields = ["id", "url", "name", "slug"]


class NestedSecretsGroupAssociationSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:secretsgroupassociation-detail")

    secret = NestedSecretSerializer()

    class Meta:
        model = models.SecretsGroupAssociation
        fields = ["id", "url", "access_type", "secret_type", "secret"]


class NestedStatusSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:status-detail")

    class Meta:
        model = models.Status
        fields = ["id", "url", "name", "slug"]


class NestedTagSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:tag-detail")

    class Meta:
        model = models.Tag
        fields = ["id", "url", "name", "slug", "color"]


class NestedWebhookSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:webhook-detail")

    class Meta:
        model = models.Webhook
        fields = ["id", "url", "name"]
