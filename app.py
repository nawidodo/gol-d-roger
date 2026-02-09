"""Flask application for Gold Portfolio Tracker."""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
from decimal import Decimal
import os

from database import init_db, SessionLocal
from models import Purchase
from galeri24 import get_gold_price

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# Initialize database
init_db()

@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Get current gold prices from Galeri24."""
    try:
        prices = get_gold_price()
        return jsonify(prices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/purchases', methods=['GET'])
def get_purchases():
    """Get all purchases."""
    db = SessionLocal()
    try:
        purchases = db.query(Purchase).order_by(Purchase.purchase_date.desc()).all()
        return jsonify([p.to_dict() for p in purchases])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/purchases', methods=['POST'])
def create_purchase():
    """Create a new purchase."""
    db = SessionLocal()
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['weight', 'purchase_price', 'total_paid', 'purchase_date']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new purchase
        purchase = Purchase(
            weight=Decimal(str(data['weight'])),
            purchase_price=Decimal(str(data['purchase_price'])),
            total_paid=Decimal(str(data['total_paid'])),
            purchase_date=datetime.fromisoformat(data['purchase_date'].replace('Z', '+00:00')),
            notes=data.get('notes', '')
        )
        
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        
        return jsonify(purchase.to_dict()), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/purchases/<int:purchase_id>', methods=['PUT'])
def update_purchase(purchase_id):
    """Update a purchase."""
    db = SessionLocal()
    try:
        purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
        if not purchase:
            return jsonify({"error": "Purchase not found"}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'weight' in data:
            purchase.weight = Decimal(str(data['weight']))
        if 'purchase_price' in data:
            purchase.purchase_price = Decimal(str(data['purchase_price']))
        if 'total_paid' in data:
            purchase.total_paid = Decimal(str(data['total_paid']))
        if 'purchase_date' in data:
            purchase.purchase_date = datetime.fromisoformat(data['purchase_date'].replace('Z', '+00:00'))
        if 'notes' in data:
            purchase.notes = data['notes']
        
        db.commit()
        db.refresh(purchase)
        
        return jsonify(purchase.to_dict())
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/purchases/<int:purchase_id>', methods=['DELETE'])
def delete_purchase(purchase_id):
    """Delete a purchase."""
    db = SessionLocal()
    try:
        purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
        if not purchase:
            return jsonify({"error": "Purchase not found"}), 404
        
        db.delete(purchase)
        db.commit()
        
        return jsonify({"message": "Purchase deleted successfully"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Get portfolio summary with current value."""
    db = SessionLocal()
    try:
        purchases = db.query(Purchase).all()
        
        # Get current prices
        current_prices = get_gold_price()
        
        if "error" in current_prices:
            return jsonify({"error": "Could not fetch current prices"}), 500
        
        # Calculate portfolio metrics
        total_weight = sum(float(p.weight) for p in purchases)
        total_invested = sum(float(p.total_paid) for p in purchases)
        
        # Calculate current value (using buy price from Galeri24)
        # We'll use the closest weight or calculate average price per gram
        current_value = 0
        if purchases and current_prices.get("data"):
            # Get average current buy price per gram from available weights
            prices_data = current_prices["data"]
            total_price = 0
            count = 0
            for weight_str, price_info in prices_data.items():
                if "buy" in price_info:
                    total_price += float(price_info["buy"])
                    count += 1
            
            if count > 0:
                avg_price_per_gram = total_price / count / float(list(prices_data.keys())[0])
                current_value = total_weight * avg_price_per_gram
        
        profit_loss = current_value - total_invested
        profit_loss_percentage = (profit_loss / total_invested * 100) if total_invested > 0 else 0
        
        return jsonify({
            "total_weight": total_weight,
            "total_invested": total_invested,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_percentage": profit_loss_percentage,
            "purchase_count": len(purchases)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
