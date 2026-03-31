from flask import Flask, request
import time

app = Flask(__name__)

HOT_PRODUCTS = {"101"}

@app.route("/product/<product_id>")
def product_page(product_id):
    client_ip = request.remote_addr
    is_hot = product_id in HOT_PRODUCTS

    print(f"[Access] Product ID: {product_id} | Hot: {is_hot} | From: {client_ip}")

    return f"""
    <html>
        <h2>Product Page: {product_id}</h2>
        <p>Status: {"Hot (Edge Cached)" if is_hot else "Normal (Cloud Cached)"}</p>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
    



