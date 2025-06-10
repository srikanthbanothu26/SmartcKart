console.log("🚀 JS File Loaded");
document.addEventListener('DOMContentLoaded', () => {
    const qtyElement = document.getElementById('qty');
    const salesPriceElement = document.getElementById('sales-price');
    const salesPriceElement2 = document.getElementById('sales-price2');
    const availabilityStatus = document.getElementById('availability-status');

    const salesPrice = parseFloat(qtyElement.dataset.price);
    const availableQty = parseInt(qtyElement.dataset.available);

    function updateStatus(qty) {
        if (qty > availableQty) {
            availabilityStatus.innerText = "Not Available";
            availabilityStatus.classList.remove('text-green-600');
            availabilityStatus.classList.add('text-red-600');
        } else {
            availabilityStatus.innerText = "Available";
            availabilityStatus.classList.remove('text-red-600');
            availabilityStatus.classList.add('text-green-600');
        }
    }

    // ✅ Initial check
    updateStatus(parseInt(qtyElement.innerText));

    // ✅ Event handlers
    document.getElementById('increment').addEventListener('click', () => {
        let qty = parseInt(qtyElement.innerText);
        qty++;
        qtyElement.innerText = qty;
        salesPriceElement.innerText = (salesPrice * qty).toFixed(2);
        salesPriceElement2.innerText = salesPriceElement.innerText;
        updateStatus(qty);
    });

    document.getElementById('decrement').addEventListener('click', () => {
        let qty = parseInt(qtyElement.innerText);
        if (qty > 1) {
            qty--;
            qtyElement.innerText = qty;
            salesPriceElement.innerText = (salesPrice * qty).toFixed(2);
            salesPriceElement2.innerText = salesPriceElement.innerText;
            updateStatus(qty);
        }
    });
    console.log("Initial qty:", qtyElement.innerText);
    console.log("Available qty:", availableQty);
    console.log("Availability element:", availabilityStatus);




    const buyNowBtn = document.getElementById('buy-now-btn');

    buyNowBtn.addEventListener('click', () => {
        const confirmed = confirm(`Do you want to order: ${qtyElement.innerText} x ${qtyElement.dataset.name}?`);
        if (confirmed) {
            fetch("/create-order/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({
                    product_id: qtyElement.dataset.productId,
                    quantity: parseInt(qtyElement.innerText),
                    Amount : salesPriceElement.innerText,
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert("✅ Order placed successfully!");
                } else {
                    alert("❌ Failed to place order.");
                }
            });
        }
    });

    function getCSRFToken() {
        return document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken'))
            ?.split('=')[1];
    }
});
