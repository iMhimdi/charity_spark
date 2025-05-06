/**
 * Donation API Interaction Functions
 */

// Make a donation
async function makeDonation(donationData) {
    try {
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        };
        
        // Add auth token if user is authenticated
        if (isAuthenticated()) {
            headers['Authorization'] = `Token ${getAuthToken()}`;
        }
        
        const response = await fetch('/api/donations/', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(donationData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data };
        }
    } catch (error) {
        console.error('Make donation error:', error);
        return { success: false, error: 'Network error occurred' };
    }
}

// Fetch donations for a campaign
async function fetchCampaignDonations(campaignId) {
    try {
        const response = await fetch(`/api/donations/?campaign=${campaignId}`);
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data };
        }
    } catch (error) {
        console.error('Fetch campaign donations error:', error);
        return { success: false, error: 'Network error occurred' };
    }
}

// Fetch user's donations
async function fetchUserDonations() {
    try {
        const response = await fetch('/api/donations/?user_donations=true', {
            headers: {
                'Authorization': `Token ${getAuthToken()}`
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, data };
        } else {
            return { success: false, error: data };
        }
    } catch (error) {
        console.error('Fetch user donations error:', error);
        return { success: false, error: 'Network error occurred' };
    }
}