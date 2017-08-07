from rest_framework_json_api import serializers
from dry_rest_permissions.generics import DRYPermissionsField
from capitolzen.organizations.models import (Organization, OrganizationInvite)


class OrganizationSerializer(serializers.ModelSerializer):
    user_is_member = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Organization
        fields = (
            'id', 'name', 'is_active', 'user_is_owner', 'billing_email', 'billing_phone',
            'user_is_admin', 'user_is_member', 'billing_address_one', 'billing_name',
            'billing_address_two', 'billing_city', 'billing_state', 'billing_zip_code',
            'stripe_payment_tokens',
        )

    def create(self, validated_data):
        org = Organization.objects.create(**validated_data)
        org.is_active = True
        org.save()
        return org


class OrganizationInviteSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = OrganizationInvite
        fields = ('id', 'organization', 'organization_name',
                  'created', 'modified', 'email', 'status',
                  'permissions')
