document.getElementById('show-register').onclick = function() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'block';
};
document.getElementById('show-login').onclick = function() {
    document.getElementById('register-section').style.display = 'none';
    document.getElementById('login-section').style.display = 'block';
};

// Registration form submit
const registerForm = document.getElementById('register-form');
registerForm.onsubmit = async function(e) {
    e.preventDefault();
    const data = {
        full_name: document.getElementById('full_name').value,
        email: document.getElementById('reg_email').value,
        mobile: document.getElementById('mobile').value,
        track: document.getElementById('track').value,
        category: document.getElementById('category').value,
        tshirt_size: document.getElementById('tshirt_size').value,
        speaker2_name: document.getElementById('speaker2_name').value,
        speaker2_email: document.getElementById('speaker2_email').value,
        speaker2_tshirt_size: document.getElementById('speaker2_tshirt_size').value,
        food_choice: document.getElementById('food_choice').value,
        blood_group: document.getElementById('blood_group').value,
        emergency_contact_name: document.getElementById('emergency_contact_name').value,
        emergency_contact_number: document.getElementById('emergency_contact_number').value,
        linkedin_url: document.getElementById('linkedin_url').value,
        sap_community_url: document.getElementById('sap_community_url').value,
        password: document.getElementById('reg_password').value,
        role: 'speaker'
    };
    const res = await fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await res.json();
    alert(result.message);
    if (result.success) {
        document.getElementById('register-section').style.display = 'none';
        document.getElementById('login-section').style.display = 'block';
    }
};

// Login form submit
const loginForm = document.getElementById('login-form');
loginForm.onsubmit = async function(e) {
    e.preventDefault();
    const data = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        role: document.getElementById('role').value
    };
    const res = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await res.json();
    alert(result.message);
    // TODO: Redirect to dashboard on success
};
