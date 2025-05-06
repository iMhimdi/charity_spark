/**
 * Campaign API Interaction Functions
 */

// Create a new campaign
async function createCampaign(campaignData) {
    try {
        const response = await fetch('/api/campaigns/', {
            method: 'POST',
            headers: {
                'Authorization': `Token ${getAuthToken()}`,
                'X-CSRFToken': getCSRFToken(),
            },
            body: campaignData // FormData object
        });
        
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data };
        }
    } catch (error) {
        console.error('Create campaign error:', error);
        return { success: false, error: 'Network error occurred' };
    }
}

// Update an existing campaign
async function updateCampaign(campaignId, campaignData) {
    try {
        const response = await fetch(`/api/campaigns/${campaignId}/`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Token ${getAuthToken()}`,
                'X-CSRFToken': getCSRFToken(),
            },
            body: campaignData // FormData object
        });
        
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data };
        }
    } catch (error) {
        console.error('Update campaign error:', error);
        return { success: false, error: 'Network error occurred' };
    }
}

// Fetch a single campaign
async function fetchCampaign(campaignId) {
    try {
        const response = await fetch(`/api/campaigns/${campaignId}/`);
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data };
        }
    } catch (error) {
        console.error('Fetch campaign error:', error);
        return { success: false, error: 'Network error occurred' };
    }
}

// Fetch campaigns with optional filters
async function fetchCampaigns(filters = {}) {
    try {
        // Build query string from filters
        const queryParams = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value) queryParams.append(key, value);
        });
        
        const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
        const response = await fetch(`/api/campaigns/${queryString}`);
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data };
        }
    } catch (error) {
        console.error('Fetch campaigns error:', error);
        return { success: false, error: 'Network error occurred' };
    }
}

// Fetch categories
async function fetchCategories() {
    try {
        const response = await fetch('/api/categories/');
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data };
        }
    } catch (error) {
        console.error('Fetch categories error:', error);
        return { success: false, error: 'Network error occurred' };
    }
}