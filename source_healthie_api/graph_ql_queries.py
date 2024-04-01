users_query = """
            query users(
                $offset: Int,
                $keywords: String,
                $sort_by: String,
                $active_status: String,
                $group_id: String,
                $show_all_by_default: Boolean,
                $should_paginate: Boolean,
                $provider_id: String,
                $conversation_id: ID,
                $limited_to_provider: Boolean,
                ) {
                usersCount(
                    keywords: $keywords,
                    active_status:$active_status,
                    group_id: $group_id,
                    conversation_id: $conversation_id,
                    provider_id: $provider_id,
                    limited_to_provider: $limited_to_provider
                )
                users(
                    offset: $offset,
                    keywords: $keywords,
                    sort_by: $sort_by,
                    active_status: $active_status,
                    group_id: $group_id,
                    conversation_id: $conversation_id,
                    show_all_by_default: $show_all_by_default,
                    should_paginate: $should_paginate,
                    provider_id: $provider_id,
                    limited_to_provider: $limited_to_provider
                ) {
                    id
                }
            }
        """

appointment_types_query = """
            query getAppointmentTypes(
                $offset: Int,
                $should_paginate: Boolean,
                $page_size: Int,
                $keywords: String,
                $show_group: Boolean,
                $provider_id: String,
                $clients_can_book: Boolean,
                $appointment_type_ids: String,
                $with_deleted_appt_types: Boolean
            ) {
                appointmentTypes(
                    offset: $offset,
                    should_paginate: $should_paginate,
                    page_size: $page_size,
                    keywords: $keywords,
                    show_group: $show_group,
                    provider_id: $provider_id,
                    clients_can_book: $clients_can_book,
                    appointment_type_ids: $appointment_type_ids,
                    with_deleted_appt_types: $with_deleted_appt_types
                ) {
                    id
                    name
                    available_contact_types
                    length
                    is_group
                    is_waitlist_enabled
                }
            }
        """

appointments_query = """
query appointments(
  $user_id: ID,
  $filter: String,
  $sort_by: String,
  $should_paginate: Boolean,
  $offset: Int,
  $is_active: Boolean,
  $with_all_statuses: Boolean
) {
  appointmentsCount(user_id: $user_id, filter: $filter, is_org: true, is_active: $is_active)
  appointments(
    is_active: $is_active,
    user_id: $user_id,
    filter: $filter,
    is_org: true,
    sort_by: $sort_by,
    should_paginate: $should_paginate,
    offset: $offset,
    with_all_statuses: $with_all_statuses
  ) {
    id
    date
    contact_type
    length
    location
    provider {
      id
      full_name
    }

    appointment_type {
      name
      id
    }

    attendees {
      id
      full_name
      first_name
      avatar_url
      phone_number
    }
  }
}
"""

available_item_types_query = """
query getAvailableItemTypes(
  $onboarding_flow_id: String
) {
  availableItemTypes(
    onboarding_flow_id: $onboarding_flow_id
  )
}
"""

conversations_query = """
query conversationMemberships(
  $offset: Int
  $keywords: String
  $active_status: String
  $client_id: String
  $read_status: String
  $conversation_type: String
  $provider_id: ID
) {
  conversationMembershipsCount(
    keywords: $keywords
    active_status: $active_status
    client_id: $client_id
    read_status: $read_status
    conversation_type: $conversation_type
    provider_id: $provider_id
  )
  conversationMemberships(
    offset: $offset
    keywords: $keywords
    active_status: $active_status
    client_id: $client_id
    read_status: $read_status
    conversation_type: $conversation_type
    provider_id: $provider_id
  ) {
    id
    display_name
    archived
    viewed
    convo {
      id
      conversation_memberships_count
    }
  }
}
"""

form_completion_requests_query = """
query requestedFormCompletions(
  $userId: ID,
  $keywords: String,
  $status: String
) {
  requestedFormCompletions(
    user_id: $userId,
    keywords: $keywords,
    status: $status
  ) {
    id
    item_type
  }
}
"""

forms_query = """
query formTemplates(
  $include_default_templates: Boolean
  $active_status: Boolean
  $should_paginate: Boolean
  $category: String
  $keywords: String
  $offset: Int
  $sortBy: String
) {
  customModuleForms(
    include_default_templates: $include_default_templates
    active_status: $active_status
    should_paginate: $should_paginate
    category: $category
    keywords: $keywords
    offset: $offset
    sort_by: $sortBy
  ) {
    id
    is_video
    name
    prefill
    uploaded_by_healthie_team
  }
}
"""

onboarding_flows_query = """
query onboardingFlows(
  $offset: Int,
  $keywords: String,
  $sort_by: String,
  $should_paginate: Boolean
) {
  onboardingFlows(
    offset: $offset,
    keywords: $keywords,
    sort_by: $sort_by,
    should_paginate: $should_paginate
  ) {
    id
    name
    is_multiple_providers
    has_forms_after_welcome
  }
}
"""

organization_members_query = """
query getOrganizationMembers(
    $offset: Int,
    $keywords: String,
    $sort_by: String,
    $licensed_in_state: String,
    $conversation_id: ID
) {
  organizationMembers(
    offset: $offset,
    keywords: $keywords,
    sort_by: $sort_by,
    licensed_in_state: $licensed_in_state,
    conversation_id: $conversation_id
  ) {
    id
    first_name
    last_name
    email
    has_api_access
  }
}
"""

programs_query = """
query courses(
  $offset: Int,
  $keywords: String,
  $course_type: String,
  $should_paginate: Boolean,
  $only_available: Boolean
) {
  courses(
    offset: $offset,
    keywords: $keywords,
    course_type: $course_type,
    should_paginate: $should_paginate,
    only_available: $only_available
  ) {
    id
    name
    description
    course_type
    course_items {
      id
      category
      item_type
      item_id
    }
    start_date
  }
}
"""

unassociated_completed_onboarding_items_query = """
query getUnassociatedCompletedOnboardingItems(
  $user_id: ID
) {
  unassociatedCompletedOnboardingItems(
    user_id: $user_id
  ) {
    id
    item_type
    item_id
    onboarding_item_id
    skipped
    user {
      id
    }
  }
}
"""

availabilities_query = """
query(
  $show_availability: Boolean,
  $one_time: Boolean,
  $is_repeating: Boolean,
  $startDate: String,
  $is_org: Boolean,
  $endDate: String
) {
  availabilities(
    show_availability: $show_availability,
    one_time: $one_time,
    is_repeating: $is_repeating,
    startDate: $startDate,
    endDate: $endDate,
    is_org: $is_org,
  ) {
    id
    day_of_week
    duration_string
    is_repeating
    range_start
    range_end
    resourceId
    timezone_abbr
    user {
      email
    }
  }
}
"""