/* script.js - Commerce Logic & Interactivity */

// --- Constants & Data ---
const PROVINCES = [
    { name: "An Giang", fee: 45000, time: "3-4 ngày" },
    { name: "Bà Rịa - Vũng Tàu", fee: 35000, time: "2-3 ngày" },
    { name: "Bạc Liêu", fee: 45000, time: "3-4 ngày" },
    { name: "Bắc Giang", fee: 85000, time: "4-5 ngày" },
    { name: "Bắc Kạn", fee: 95000, time: "5-6 ngày" },
    { name: "Bắc Ninh", fee: 85000, time: "4-5 ngày" },
    { name: "Bến Tre", fee: 40000, time: "3-4 ngày" },
    { name: "Bình Dương", fee: 30000, time: "2-3 ngày" },
    { name: "Bình Định", fee: 40000, time: "2-3 ngày" },
    { name: "Bình Phước", fee: 35000, time: "2-3 ngày" },
    { name: "Bình Thuận", fee: 30000, time: "2-3 ngày" },
    { name: "Cà Mau", fee: 50000, time: "4-5 ngày" },
    { name: "Cao Bằng", fee: 110000, time: "5-6 ngày" },
    { name: "Cần Thơ", fee: 40000, time: "3-4 ngày" },
    { name: "Đà Nẵng", fee: 45000, time: "2-3 ngày" },
    { name: "Đắk Lắk", fee: 25000, time: "1-2 ngày" },
    { name: "Đắk Nông", fee: 25000, time: "1-2 ngày" },
    { name: "Điện Biên", fee: 120000, time: "6-7 ngày" },
    { name: "Đồng Nai", fee: 30000, time: "2-3 ngày" },
    { name: "Đồng Tháp", fee: 40000, time: "3-4 ngày" },
    { name: "Gia Lai", fee: 30000, time: "1-2 ngày" },
    { name: "Hà Giang", fee: 120000, time: "6-7 ngày" },
    { name: "Hà Nam", fee: 85000, time: "4-5 ngày" },
    { name: "Hà Nội", fee: 80000, time: "4-5 ngày" },
    { name: "Hà Tĩnh", fee: 65000, time: "3-4 ngày" },
    { name: "Hải Dương", fee: 85000, time: "4-5 ngày" },
    { name: "Hải Phòng", fee: 85000, time: "4-5 ngày" },
    { name: "Hậu Giang", fee: 45000, time: "3-4 ngày" },
    { name: "Hòa Bình", fee: 90000, time: "4-5 ngày" },
    { name: "Hưng Yên", fee: 85000, time: "4-5 ngày" },
    { name: "Khánh Hòa", fee: 30000, time: "1-2 ngày" },
    { name: "Kiên Giang", fee: 50000, time: "4-5 ngày" },
    { name: "Kon Tum", fee: 35000, time: "1-2 ngày" },
    { name: "Lai Châu", fee: 120000, time: "6-7 ngày" },
    { name: "Lạng Sơn", fee: 100000, time: "5-6 ngày" },
    { name: "Lào Cai", fee: 110000, time: "5-6 ngày" },
    { name: "Lâm Đồng", fee: 0, time: "1-2 ngày" },
    { name: "Long An", fee: 35000, time: "2-3 ngày" },
    { name: "Nam Định", fee: 85000, time: "4-5 ngày" },
    { name: "Nghệ An", fee: 70000, time: "3-4 ngày" },
    { name: "Ninh Bình", fee: 85000, time: "4-5 ngày" },
    { name: "Ninh Thuận", fee: 25000, time: "1-2 ngày" },
    { name: "Phú Thọ", fee: 90000, time: "4-5 ngày" },
    { name: "Phú Yên", fee: 35000, time: "2-3 ngày" },
    { name: "Quảng Bình", fee: 60000, time: "3-4 ngày" },
    { name: "Quảng Nam", fee: 50000, time: "2-3 ngày" },
    { name: "Quảng Ngãi", fee: 45000, time: "2-3 ngày" },
    { name: "Quảng Ninh", fee: 95000, time: "5-6 ngày" },
    { name: "Quảng Trị", fee: 55000, time: "3-4 ngày" },
    { name: "Sóc Trăng", fee: 45000, time: "3-4 ngày" },
    { name: "Sơn La", fee: 110000, time: "5-6 ngày" },
    { name: "Tây Ninh", fee: 35000, time: "2-3 ngày" },
    { name: "Thái Bình", fee: 85000, time: "4-5 ngày" },
    { name: "Thái Nguyên", fee: 90000, time: "4-5 ngày" },
    { name: "Thanh Hóa", fee: 75000, time: "3-4 ngày" },
    { name: "Thừa Thiên Huế", fee: 50000, time: "2-3 ngày" },
    { name: "Tiền Giang", fee: 40000, time: "3-4 ngày" },
    { name: "TP Hồ Chí Minh", fee: 30000, time: "2-3 ngày" },
    { name: "Trà Vinh", fee: 45000, time: "3-4 ngày" },
    { name: "Tuyên Quang", fee: 100000, time: "5-6 ngày" },
    { name: "Vĩnh Long", fee: 40000, time: "3-4 ngày" },
    { name: "Vĩnh Phúc", fee: 85000, time: "4-5 ngày" },
    { name: "Yên Bái", fee: 100000, time: "5-6 ngày" }
];

// --- Application State ---
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let products = [];
let isDarkMode = localStorage.getItem('theme') === 'dark';
let currentUser = JSON.parse(localStorage.getItem('user')) || null;
let selectedShippingFee = 0;
let selectedPaymentMethod = '';
let selectedPaymentType = 'full';

// --- Selectors ---
const productList = document.getElementById('product-list');
const cartCount = document.getElementById('cart-count');
const cartItemsList = document.getElementById('cart-items-list');
const totalPriceEl = document.getElementById('total-price');
const subtotalEl = document.getElementById('subtotal');
const shippingFeeEl = document.getElementById('shipping-fee');
const deliveryTimeEl = document.getElementById('delivery-time');
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const cartBtn = document.getElementById('cart-btn');
const backToHome = document.getElementById('back-to-home');
const logoBtn = document.getElementById('logo-btn');
const homeSection = document.getElementById('home-section');
const cartSection = document.getElementById('cart-section');
const searchInput = document.getElementById('search-input');
const toastContainer = document.getElementById('toast-container');
const provinceSelect = document.getElementById('cust-province');
const adminSection = document.getElementById('admin-section');
const adminBtn = document.getElementById('admin-btn');
const adminProductList = document.getElementById('admin-product-list');
const adminOrderList = document.getElementById('admin-order-list');
const productForm = document.getElementById('product-form');
const ordersSection = document.getElementById('orders-section');
const ordersBtn = document.getElementById('orders-btn');
const myOrdersList = document.getElementById('my-orders-list');

// Auth Selectors
const authBtn = document.getElementById('auth-btn');
const userDisplayName = document.getElementById('user-display-name');
const authModal = document.getElementById('auth-modal');
const closeAuth = document.getElementById('close-auth');
const loginContainer = document.getElementById('login-form-container');
const registerContainer = document.getElementById('register-form-container');
const forgotContainer = document.getElementById('forgot-form-container');
const resetContainer = document.getElementById('reset-form-container');
const profileContainer = document.getElementById('profile-container');

// Chat & Review Selectors
const chatToggle = document.getElementById('chat-toggle');
const chatWindow = document.getElementById('chat-window');
const closeChat = document.getElementById('close-chat');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendMsgBtn = document.getElementById('send-msg-btn');
const reviewModal = document.getElementById('review-modal');
const closeReview = document.getElementById('close-review');
const submitReviewBtn = document.getElementById('submit-review-btn');
const productDetailModal = document.getElementById('product-detail-modal');
const closeDetail = document.getElementById('close-detail');

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initProvinces();
    initPaymentHandlers();
    initAuthHandlers();
    fetchProducts();
    updateCartUI();
    updateAuthUI();
    checkForReset();
    initAdminHandlers();
    initChat();
    initReviewHandlers();

    const checkoutBtn = document.querySelector('#cart-section .btn-primary');
    if (checkoutBtn) checkoutBtn.addEventListener('click', handleCheckout);

    if (provinceSelect) {
        provinceSelect.addEventListener('change', (e) => {
            const provinceName = e.target.value;
            const province = PROVINCES.find(p => p.name === provinceName);
            if (province) {
                selectedShippingFee = province.fee;
                deliveryTimeEl.textContent = `Dự kiến giao hàng: ${province.time}`;
                updateCartUI();
            }
        });
    }
});

function initProvinces() {
    if (!provinceSelect) return;
    PROVINCES.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.name;
        opt.textContent = p.name;
        provinceSelect.appendChild(opt);
    });
}

function initPaymentHandlers() {
    const cards = document.querySelectorAll('.payment-card');
    const subBtns = document.querySelectorAll('.sub-opt-btn');
    const bankOptions = document.getElementById('bank-sub-options');
    const bankDetails = document.getElementById('bank-details');

    cards.forEach(card => {
        card.addEventListener('click', () => {
            cards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            selectedPaymentMethod = card.dataset.method;
            if (selectedPaymentMethod === 'bank') {
                bankOptions.style.display = 'flex';
                bankDetails.style.display = 'block';
            } else {
                bankOptions.style.display = 'none';
                bankDetails.style.display = 'none';
            }
        });
    });

    subBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            subBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedPaymentType = btn.dataset.type;
        });
    });
}

// --- Auth Interactivity ---
function initAuthHandlers() {
    authBtn.addEventListener('click', () => {
        authModal.style.display = 'flex';
        showAuthForm(currentUser ? 'profile' : 'login');
    });

    closeAuth.addEventListener('click', () => authModal.style.display = 'none');
    window.addEventListener('click', (e) => { if (e.target === authModal) authModal.style.display = 'none'; });

    document.getElementById('to-register').addEventListener('click', (e) => { e.preventDefault(); showAuthForm('register'); });
    document.getElementById('to-login').addEventListener('click', (e) => { e.preventDefault(); showAuthForm('login'); });
    document.getElementById('to-forgot').addEventListener('click', (e) => { e.preventDefault(); showAuthForm('forgot'); });
    document.getElementById('back-to-login').addEventListener('click', (e) => { e.preventDefault(); showAuthForm('login'); });

    document.getElementById('login-submit').addEventListener('click', handleLogin);
    document.getElementById('reg-submit').addEventListener('click', handleRegister);
    document.getElementById('forgot-submit').addEventListener('click', handleForgot);
    document.getElementById('reset-submit').addEventListener('click', handleReset);
    document.getElementById('logout-submit').addEventListener('click', handleLogout);
}

function showAuthForm(type) {
    [loginContainer, registerContainer, forgotContainer, resetContainer, profileContainer].forEach(c => c.style.display = 'none');
    if (type === 'login') loginContainer.style.display = 'block';
    else if (type === 'register') registerContainer.style.display = 'block';
    else if (type === 'forgot') forgotContainer.style.display = 'block';
    else if (type === 'reset') resetContainer.style.display = 'block';
    else if (type === 'profile') {
        profileContainer.style.display = 'block';
        if (currentUser) {
            document.getElementById('profile-user-name').textContent = currentUser.name;
            document.getElementById('profile-user-email').textContent = currentUser.email;
        }
    }
}

async function handleLogin() {
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value.trim();
    if (!email || !password) return alert("Vui lòng nhập đủ thông tin!");

    try {
        const res = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (data.status === 'success') {
            currentUser = data.user;
            localStorage.setItem('user', JSON.stringify(currentUser));
            updateAuthUI();
            authModal.style.display = 'none';
            showToast("Chào mừng bạn quay trở lại!");
        } else {
            alert(data.message);
        }
    } catch (err) { alert("Lỗi kết nối server!"); }
}

async function handleRegister() {
    const name = document.getElementById('reg-name').value.trim();
    const email = document.getElementById('reg-email').value.trim();
    const password = document.getElementById('reg-password').value.trim();
    const confirm = document.getElementById('reg-confirm-password').value.trim();

    if (!name || !email || !password) return alert("Vui lòng nhập đủ!");
    if (password !== confirm) return alert("Mật khẩu không khớp!");

    try {
        const res = await fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        const data = await res.json();
        if (data.status === 'success') {
            alert("Đăng ký thành công! Hãy đăng nhập nhé.");
            showAuthForm('login');
        } else { alert(data.message); }
    } catch (err) { alert("Lỗi kết nối!"); }
}

async function handleForgot() {
    const email = document.getElementById('forgot-email').value.trim();
    if (!email) return alert("Nhập email!");
    const res = await fetch('/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
    });
    const data = await res.json();
    alert(data.message);
}

function checkForReset() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('email') && urlParams.has('token')) {
        authModal.style.display = 'flex';
        showAuthForm('reset');
    }
}

async function handleReset() {
    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get('email');
    const token = urlParams.get('token');
    const password = document.getElementById('reset-password').value.trim();
    const confirm = document.getElementById('reset-confirm').value.trim();

    if (!token) return alert("Liên kết không hợp lệ!");
    if (!password) return alert("Nhập mật khẩu mới!");
    if (password !== confirm) return alert("Mật khẩu không khớp!");

    try {
        const res = await fetch('/reset-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, token })
        });
        const data = await res.json();
        if (data.status === 'success') {
            alert(data.message);
            window.history.replaceState({}, document.title, "/");
            showAuthForm('login');
        } else {
            alert(data.message);
        }
    } catch (err) { alert("Lỗi khi reset mật khẩu!"); }
}

function handleLogout() {
    currentUser = null;
    localStorage.removeItem('user');
    updateAuthUI();
    authModal.style.display = 'none';

    const authInputs = document.querySelectorAll('#auth-modal input');
    authInputs.forEach(input => {
        input.value = '';
        if (input.type === 'text' && (input.id.includes('password') || input.id.includes('pass'))) {
            input.type = 'password';
        }
    });

    showToast("Đã đăng xuất.");
}

window.togglePass = (id, icon) => {
    const input = document.getElementById(id);
    if (input.type === 'password') {
        input.type = 'text';
        icon.setAttribute('data-lucide', 'eye-off');
    } else {
        input.type = 'password';
        icon.setAttribute('data-lucide', 'eye');
    }
    lucide.createIcons();
};

function updateAuthUI() {
    if (currentUser) {
        userDisplayName.textContent = currentUser.name;
        userDisplayName.style.display = 'inline-block';
        ordersBtn.style.display = 'inline-block';
        if (currentUser.role === 'admin') {
            adminBtn.style.display = 'inline-block';
        } else {
            adminBtn.style.display = 'none';
        }
    } else {
        userDisplayName.style.display = 'none';
        adminBtn.style.display = 'none';
        ordersBtn.style.display = 'none';
    }
}

// --- Chat Logic ---
let chatInterval = null;

function initChat() {
    if (!chatToggle) return;

    chatToggle.addEventListener('click', () => {
        const isVisible = chatWindow.style.display === 'flex';
        chatWindow.style.display = isVisible ? 'none' : 'flex';
        if (!isVisible) {
            fetchMessages();
            if (!chatInterval) chatInterval = setInterval(fetchMessages, 3000);
        } else {
            clearInterval(chatInterval);
            chatInterval = null;
        }
    });

    closeChat.addEventListener('click', () => {
        chatWindow.style.display = 'none';
        clearInterval(chatInterval);
        chatInterval = null;
    });

    sendMsgBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
}

async function fetchMessages() {
    if (!currentUser) return;
    try {
        const res = await fetch(`/api/messages?email=${encodeURIComponent(currentUser.email)}`);
        const messages = await res.json();
        renderMessages(messages);
    } catch (err) { console.error("Lỗi tải tin nhắn"); }
}

function renderMessages(messages) {
    const html = messages.map(m => `
        <div class="message ${m.sender_role === 'admin' ? 'admin' : 'user'}">
            ${m.content}
            <div style="font-size: 0.6rem; opacity: 0.6; margin-top: 0.25rem;">${m.time.split(' ')[1]}</div>
        </div>
    `).join('');

    const welcome = '<div class="message admin">Xin chào! Chúng tôi có thể giúp gì cho bạn?</div>';
    chatMessages.innerHTML = welcome + html;
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
    const content = chatInput.value.trim();
    if (!content || !currentUser) return;

    chatInput.value = '';
    try {
        await fetch('/api/messages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_email: currentUser.email,
                content: content,
                sender_role: 'user'
            })
        });
        fetchMessages();
    } catch (err) { showToast("Không gửi được tin nhắn", "error"); }
}

// --- Review Logic ---
let currentReviewOrderId = null;
let currentReviewProductId = null;

function initReviewHandlers() {
    if (closeReview) closeReview.addEventListener('click', () => reviewModal.style.display = 'none');
    if (submitReviewBtn) submitReviewBtn.addEventListener('click', submitReview);
    if (closeDetail) closeDetail.addEventListener('click', () => productDetailModal.style.display = 'none');

    window.addEventListener('click', (e) => {
        if (e.target === reviewModal) reviewModal.style.display = 'none';
        if (e.target === productDetailModal) productDetailModal.style.display = 'none';
    });
}

window.openReviewModal = (orderId, productId, productName, productImage) => {
    currentReviewOrderId = orderId;
    currentReviewProductId = productId;

    document.getElementById('review-product-info').innerHTML = `
        <img src="static/${productImage}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px;">
        <div>
            <div style="font-weight: 700;">${productName}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">Đơn hàng #${orderId}</div>
        </div>
    `;

    document.querySelectorAll('input[name="rating"]').forEach(r => r.checked = false);
    document.getElementById('review-comment').value = '';
    reviewModal.style.display = 'flex';
};

async function submitReview() {
    const rating = document.querySelector('input[name="rating"]:checked')?.value;
    const comment = document.getElementById('review-comment').value.trim();

    if (!rating) return alert("Vui lòng chọn số sao đánh giá!");
    if (!comment) return alert("Vui lòng nhập nhận xét của bạn!");

    try {
        const res = await fetch('/api/reviews', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                order_id: currentReviewOrderId,
                product_id: currentReviewProductId,
                user_email: currentUser.email,
                user_name: currentUser.name,
                rating: parseInt(rating),
                comment: comment
            })
        });
        const data = await res.json();
        if (data.status === 'success') {
            showToast("Cảm ơn bạn đã đánh giá!");
            reviewModal.style.display = 'none';
            fetchMyOrders();
        } else {
            alert(data.message);
        }
    } catch (err) { alert("Lỗi khi gửi đánh giá!"); }
}

window.showProductDetail = async (productId) => {
    const product = products.find(p => p.id === productId);
    if (!product) return;

    try {
        const res = await fetch(`/api/reviews/${productId}`);
        const reviews = await res.json();

        const avgRating = reviews.length > 0
            ? (reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1)
            : "0.0";

        const reviewsHtml = reviews.length > 0 ? reviews.map(r => `
            <div class="review-card">
                <div class="review-avatar">${r.user_name.charAt(0).toUpperCase()}</div>
                <div class="review-content">
                    <div class="review-header">
                        <span class="review-name">${r.user_name}</span>
                        <span class="review-date">${r.time.split(' ')[0]}</span>
                    </div>
                    <div class="star-rating" style="margin-bottom: 0.5rem;">
                        ${'★'.repeat(r.rating)}${'☆'.repeat(5 - r.rating)}
                    </div>
                    <p style="font-size: 0.9rem; line-height: 1.5;">${r.comment}</p>
                </div>
            </div>
        `).join('') : '<p style="text-align: center; padding: 2rem; color: var(--text-muted);">Chưa có đánh giá nào cho sản phẩm này.</p>';

        document.getElementById('product-detail-body').innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 2rem; margin-bottom: 2rem;">
                <img src="static/${product.image}" style="width: 100%; border-radius: var(--radius-lg); box-shadow: var(--shadow-md);">
                <div>
                    <span class="product-category">${product.category}</span>
                    <h2 style="font-size: 1.75rem; margin: 0.5rem 0;">${product.name}</h2>
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                        <div class="star-rating">${'★'.repeat(Math.round(avgRating))}${'☆'.repeat(5 - Math.round(avgRating))}</div>
                        <span style="font-weight: 600;">${avgRating}</span>
                        <span style="color: var(--text-muted); font-size: 0.85rem;">(${reviews.length} đánh giá)</span>
                    </div>
                    <p class="product-price" style="font-size: 1.5rem; margin-bottom: 1.5rem;">${formatPrice(product.price)}</p>
                    <button class="btn-primary" style="width: 100%; padding: 1rem;" onclick="addToCart(${product.id}); document.getElementById('product-detail-modal').style.display='none';">Thêm vào giỏ hàng</button>
                    <p style="margin-top: 1.5rem; color: var(--text-muted); font-size: 0.9rem; line-height: 1.6;">Sản phẩm chính hãng 100%. Bảo hành 12 tháng tại các trung tâm bảo hành ủy quyền toàn quốc. Giao hàng nhanh chóng trong 24h.</p>
                </div>
            </div>
            <div style="border-top: 1px solid var(--border-color); padding-top: 2rem;">
                <h3 style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
                    <i data-lucide="message-square" size="20"></i> Đánh giá từ khách hàng
                </h3>
                ${reviewsHtml}
            </div>
        `;

        productDetailModal.style.display = 'flex';
        lucide.createIcons();
    } catch (err) { alert("Không thể tải thông tin đánh giá."); }
};

// --- Admin Dashboard Logic ---
function initAdminHandlers() {
    if (!adminBtn) return;
    adminBtn.addEventListener('click', () => showSection('admin'));
    if (productForm) productForm.addEventListener('submit', handleProductSubmit);
    const cancelBtn = document.getElementById('p-cancel-btn');
    if (cancelBtn) cancelBtn.addEventListener('click', resetProductForm);
}

async function switchAdminTab(tab) {
    const prodContent = document.getElementById('admin-products-content');
    const orderContent = document.getElementById('admin-orders-content');
    const msgContent = document.getElementById('admin-messages-content');
    const tabs = document.querySelectorAll('.admin-tab');

    prodContent.style.display = tab === 'products' ? 'block' : 'none';
    orderContent.style.display = tab === 'orders' ? 'block' : 'none';
    msgContent.style.display = tab === 'messages' ? 'block' : 'none';

    tabs.forEach(btn => {
        const id = btn.id.split('-')[1];
        btn.classList.toggle('active', id === tab);
    });

    if (tab === 'products') fetchAdminProducts();
    if (tab === 'orders') fetchOrders();
    if (tab === 'messages') fetchAdminMessages();
}

async function fetchAdminMessages() {
    try {
        const res = await fetch('/api/messages?admin=true');
        const data = await res.json();
        const grouped = {};
        data.forEach(m => {
            if (!grouped[m.user_email]) grouped[m.user_email] = [];
            grouped[m.user_email].push(m);
        });

        const listEl = document.getElementById('admin-chat-list');
        if (Object.keys(grouped).length === 0) {
            listEl.innerHTML = '<p style="text-align: center; color: var(--text-muted); padding: 2rem;">Chưa có tin nhắn nào.</p>';
            return;
        }

        listEl.innerHTML = Object.entries(grouped).map(([email, msgs]) => {
            const lastMsg = msgs[msgs.length - 1];
            return `
                <div style="background: var(--bg-color); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color); cursor: pointer; margin-bottom: 1rem;" onclick="openAdminReply('${email}')">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="font-weight: 700;">${email}</span>
                        <span style="font-size: 0.75rem; color: var(--text-muted);">${lastMsg.time}</span>
                    </div>
                    <div style="font-size: 0.9rem; color: var(--text-main); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        ${lastMsg.sender_role === 'admin' ? '<b>Bạn:</b> ' : ''}${lastMsg.content}
                    </div>
                </div>
            `;
        }).join('');
    } catch (err) { console.error("Lỗi tải tin nhắn admin"); }
}

window.openAdminReply = (email) => {
    const content = prompt(`Trả lời khách hàng ${email}:`);
    if (!content) return;

    fetch('/api/messages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_email: email,
            content: content,
            sender_role: 'admin'
        })
    }).then(() => {
        showToast("Đã gửi phản hồi");
        fetchAdminMessages();
    });
};

async function fetchAdminProducts() {
    const res = await fetch('/products');
    const data = await res.json();
    renderAdminProducts(data);
}

function renderAdminProducts(items) {
    if (!adminProductList) return;
    adminProductList.innerHTML = items.map(p => `
        <tr>
            <td style="padding: 1rem;"><img src="static/${p.image}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;"></td>
            <td style="padding: 1rem;">
                <div style="font-weight: 600;">${p.name}</div>
                <div style="font-size: 0.8rem; color: var(--accent-color);">${p.price.toLocaleString()}đ</div>
            </td>
            <td style="padding: 1rem;">
                <button class="action-btn edit-btn" onclick="editProduct(${p.id})"><i data-lucide="edit-2" size="14"></i> Sửa</button>
                <button class="action-btn delete-btn" onclick="deleteProduct(${p.id})"><i data-lucide="trash-2" size="14"></i> Xóa</button>
            </td>
        </tr>
    `).join('');
    lucide.createIcons();
}

async function handleProductSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('edit-product-id').value;
    const formData = new FormData();
    formData.append('name', document.getElementById('p-name').value);
    formData.append('price', document.getElementById('p-price').value);
    formData.append('category', document.getElementById('p-category').value);
    const imageFile = document.getElementById('p-image').files[0];
    if (imageFile) formData.append('image', imageFile);

    const url = id ? `/api/products/${id}` : '/api/products';
    const method = id ? 'PUT' : 'POST';
    try {
        const res = await fetch(url, { method, body: formData });
        const data = await res.json();
        if (data.status === 'success') {
            showToast(data.message);
            resetProductForm();
            fetchAdminProducts();
            fetchProducts();
        } else { alert(data.message); }
    } catch (err) { alert("Lỗi khi lưu sản phẩm!"); }
}

function editProduct(id) {
    const p = products.find(prod => prod.id === id);
    if (!p) return;
    document.getElementById('edit-product-id').value = p.id;
    document.getElementById('p-name').value = p.name;
    document.getElementById('p-price').value = p.price;
    document.getElementById('p-category').value = p.category;
    document.getElementById('admin-form-title').textContent = "Chỉnh sửa sản phẩm";
    document.getElementById('p-submit-btn').textContent = "Cập nhật sản phẩm";
    document.getElementById('p-cancel-btn').style.display = 'inline-block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetProductForm() {
    document.getElementById('edit-product-id').value = '';
    productForm.reset();
    document.getElementById('admin-form-title').textContent = "Thêm sản phẩm mới";
    document.getElementById('p-submit-btn').textContent = "Lưu sản phẩm";
    document.getElementById('p-cancel-btn').style.display = 'none';
}

async function deleteProduct(id) {
    if (!confirm("Bạn có chắc chắn muốn xóa sản phẩm này?")) return;
    try {
        const res = await fetch(`/api/products/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.status === 'success') {
            showToast(data.message);
            fetchAdminProducts();
            fetchProducts();
        } else { alert(data.message); }
    } catch (err) { alert("Lỗi khi xóa sản phẩm!"); }
}

async function fetchOrders() {
    const res = await fetch('/api/orders');
    const data = await res.json();
    renderAdminOrders(data);
}

function renderAdminOrders(orders) {
    if (!adminOrderList) return;
    const statusConfig = {
        'Chờ xử lý': { bg: '#fef3c7', color: '#92400e', icon: 'clock' },
        'Đang giao': { bg: '#dbeafe', color: '#1e40af', icon: 'truck' },
        'Đã giao': { bg: '#d1fae5', color: '#065f46', icon: 'check-circle' },
        'Đã hủy': { bg: '#fee2e2', color: '#991b1b', icon: 'x-circle' }
    };
    adminOrderList.innerHTML = orders.map(o => {
        const st = statusConfig[o.status] || statusConfig['Chờ xử lý'];
        return `
        <tr data-order-id="${o.id}">
            <td style="padding:1rem;">#${o.id}</td>
            <td style="padding:1rem;">${o.customer?.name}<br><small>${o.customer?.phone}</small></td>
            <td style="padding:1rem;">${o.total.toLocaleString()}đ</td>
            <td style="padding:1rem;"><span style="background:${st.bg}; color:${st.color}; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:700;">${o.status}</span></td>
            <td style="padding:1rem;">
                <div style="display:flex; gap:0.5rem;">
                    <button class="action-btn" onclick="updateOrderStatus(${o.id}, 'Đang giao')">Giao</button>
                    <button class="action-btn" onclick="updateOrderStatus(${o.id}, 'Đã giao')">Xong</button>
                    <button class="action-btn delete-btn" onclick="deleteOrder(${o.id})">Xóa</button>
                </div>
            </td>
        </tr>`;
    }).join('');
    lucide.createIcons();
}

window.updateOrderStatus = async function (orderId, newStatus) {
    await fetch(`/api/orders/${orderId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
    });
    fetchOrders();
};

window.deleteOrder = async function (orderId) {
    if (!confirm("Xóa đơn hàng này?")) return;
    await fetch(`/api/orders/${orderId}`, { method: 'DELETE' });
    fetchOrders();
};

// --- User Order Tracking ---
async function fetchMyOrders() {
    if (!currentUser) return;
    try {
        const res = await fetch(`/api/my-orders?email=${encodeURIComponent(currentUser.email)}`);
        const data = await res.json();
        renderMyOrders(data);
    } catch (err) { console.error("Lỗi đơn hàng"); }
}

function renderMyOrders(orders) {
    if (!myOrdersList) return;
    if (orders.length === 0) {
        myOrdersList.innerHTML = '<p style="text-align:center; padding:3rem; color:var(--text-muted);">Bạn chưa có đơn hàng nào.</p>';
        return;
    }
    const statusColors = {
        'Chờ xử lý': { bg: '#fef3c7', color: '#92400e', icon: 'clock' },
        'Đang giao': { bg: '#dbeafe', color: '#1e40af', icon: 'truck' },
        'Đã giao': { bg: '#d1fae5', color: '#065f46', icon: 'check-circle' },
        'Đã hủy': { bg: '#fee2e2', color: '#991b1b', icon: 'x-circle' }
    };

    myOrdersList.innerHTML = orders.map(o => {
        const st = statusColors[o.status] || statusColors['Chờ xử lý'];
        const itemsHtml = o.items.map(item => `
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem 0; border-bottom: 1px dashed var(--border-color);">
                <img src="static/${item.image}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px;">
                <div style="flex: 1;">
                    <div style="font-weight: 600;">${item.name}</div>
                    <div style="font-size: 0.85rem; color: var(--text-muted);">Số lượng: ${item.quantity}</div>
                    ${o.status === 'Đã giao' ? `
                        <button class="order-review-btn" onclick="openReviewModal(${o.id}, ${item.id}, '${item.name}', '${item.image}')">
                            <i data-lucide="star" size="14"></i> Đánh giá ngay
                        </button>
                    ` : ''}
                </div>
                <div style="font-weight: 700; color: var(--accent-color);">${item.price.toLocaleString()}đ</div>
            </div>
        `).join('');

        return `
        <div style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: var(--shadow-sm);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color);">
                <div>
                    <div style="font-size: 0.8rem; color: var(--text-muted); font-family: monospace;">Mã đơn: #${o.id}</div>
                    <div style="font-size: 0.85rem; font-weight: 600;">${o.time}</div>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; background: ${st.bg}; color: ${st.color}; padding: 0.4rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">
                    <i data-lucide="${st.icon}" size="14"></i> ${o.status}
                </div>
            </div>
            ${itemsHtml}
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                <div style="font-size: 0.9rem; color: var(--text-muted);">
                    <i data-lucide="map-pin" size="16"></i> ${o.customer.address}, ${o.customer.province}
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.85rem;">Tổng cộng</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: var(--accent-color);">${o.total.toLocaleString()}đ</div>
                </div>
            </div>
        </div>
        `;
    }).join('');
    lucide.createIcons();
}

// --- Theme Management ---
function initTheme() {
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeIcon.setAttribute('data-lucide', 'moon');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        themeIcon.setAttribute('data-lucide', 'sun');
    }
    lucide.createIcons();
}

themeToggle.addEventListener('click', () => {
    isDarkMode = !isDarkMode;
    document.documentElement.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
    themeIcon.setAttribute('data-lucide', isDarkMode ? 'moon' : 'sun');
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    lucide.createIcons();
});

// --- API Fetching ---
async function fetchProducts() {
    try {
        const response = await fetch('/products');
        products = await response.json();
        renderProducts(products);
    } catch (error) { console.error("Lỗi API sản phẩm"); }
}

function renderProducts(items) {
    productList.innerHTML = '';
    if (items.length === 0) {
        productList.innerHTML = '<p style="grid-column:1/-1; text-align:center; padding:3rem;">Không có sản phẩm nào.</p>';
        return;
    }
    items.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <div class="product-img-wrapper" onclick="showProductDetail(${product.id})">
                <img src="static/${product.image}" alt="${product.name}" class="product-img">
            </div>
            <div class="product-info">
                <span class="product-category">${product.category}</span>
                <h3 class="product-title" onclick="showProductDetail(${product.id})" style="cursor: pointer;">${product.name}</h3>
                <p class="product-price">${formatPrice(product.price)}</p>
                <button class="add-to-cart" onclick="addToCart(${product.id})">Thêm vào giỏ</button>
            </div>
        `;
        productList.appendChild(card);
    });
}

// --- Cart Logic ---
window.addToCart = (productId) => {
    const product = products.find(p => p.id === productId);
    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) existingItem.quantity += 1;
    else cart.push({ ...product, quantity: 1 });
    saveCart();
    updateCartUI();
    showToast(`Đã thêm ${product.name} vào giỏ!`);
};

window.removeFromCart = (productId) => {
    cart = cart.filter(item => item.id !== productId);
    saveCart();
    updateCartUI();
};

window.updateQuantity = (productId, delta) => {
    const item = cart.find(i => i.id === productId);
    if (item) {
        item.quantity += delta;
        if (item.quantity <= 0) removeFromCart(productId);
        else { saveCart(); updateCartUI(); }
    }
};

function saveCart() { localStorage.setItem('cart', JSON.stringify(cart)); }

function updateCartUI() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;

    if (!cartItemsList) return;
    if (cart.length === 0) {
        cartItemsList.innerHTML = '<p>Giỏ hàng đang trống.</p>';
        subtotalEl.textContent = '0đ';
        shippingFeeEl.textContent = '0đ';
        totalPriceEl.textContent = '0đ';
        return;
    }

    cartItemsList.innerHTML = cart.map(item => `
        <div class="cart-item">
            <img src="static/${item.image}" alt="${item.name}">
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <p>${formatPrice(item.price)}</p>
                <div class="quantity-controls">
                    <button onclick="updateQuantity(${item.id}, -1)">-</button>
                    <span>${item.quantity}</span>
                    <button onclick="updateQuantity(${item.id}, 1)">+</button>
                </div>
            </div>
            <button class="remove-item" onclick="removeFromCart(${item.id})">
                <i data-lucide="trash-2" size="18"></i>
            </button>
        </div>
    `).join('');

    const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    subtotalEl.textContent = formatPrice(subtotal);
    shippingFeeEl.textContent = formatPrice(selectedShippingFee);
    totalPriceEl.textContent = formatPrice(subtotal + selectedShippingFee);

    lucide.createIcons();
}

function formatPrice(price) { return price.toLocaleString() + 'đ'; }

function showSection(sectionId) {
    [homeSection, cartSection, adminSection, ordersSection].forEach(s => s.style.display = 'none');
    document.getElementById(`${sectionId}-section`).style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });

    if (sectionId === 'admin') switchAdminTab('products');
    if (sectionId === 'orders') fetchMyOrders();
}

cartBtn.addEventListener('click', () => showSection('cart'));
backToHome.addEventListener('click', () => showSection('home'));
logoBtn.addEventListener('click', () => showSection('home'));
ordersBtn.addEventListener('click', () => showSection('orders'));

// --- Toast Helper ---
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i data-lucide="${type === 'success' ? 'check-circle' : 'alert-circle'}"></i>
        <span>${message}</span>
    `;
    toastContainer.appendChild(toast);
    lucide.createIcons();
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

async function handleCheckout() {
    if (cart.length === 0) return alert("Giỏ hàng đang trống!");
    if (!selectedPaymentMethod) return alert("Vui lòng chọn phương thức thanh toán!");

    const name = document.getElementById('cust-name').value.trim();
    const phone = document.getElementById('cust-phone').value.trim();
    const address = document.getElementById('cust-address').value.trim();
    const province = provinceSelect.value;

    if (!name || !phone || !address || !province) return alert("Vui lòng điền đủ thông tin!");

    const orderData = {
        customer: { name, phone, address, province, email: currentUser ? currentUser.email : null },
        items: cart,
        subtotal: cart.reduce((sum, item) => sum + item.price * item.quantity, 0),
        shipping_fee: selectedShippingFee,
        total: cart.reduce((sum, item) => sum + item.price * item.quantity, 0) + selectedShippingFee,
        payment: { method: selectedPaymentMethod, type: selectedPaymentType }
    };

    try {
        const res = await fetch('/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData)
        });
        const data = await res.json();
        if (data.status === 'success') {
            showToast("Đặt hàng thành công!");
            cart = [];
            saveCart();
            updateCartUI();
            showSection('home');
        } else { alert(data.message); }
    } catch (err) { alert("Lỗi đặt hàng!"); }
}

// Basic Search
searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    const filtered = products.filter(p =>
        p.name.toLowerCase().includes(query) ||
        p.category.toLowerCase().includes(query)
    );
    renderProducts(filtered);
});
