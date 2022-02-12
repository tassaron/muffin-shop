import React, { Component } from "react";


class CartPageRow extends Component {
    render() {
        return (
            <div className="CartPage-row row" data-product-id={this.props.data.id}>
                <div className="CartPage-name col-12 text-center text-uppercase product-title">{this.props.data.name}</div>
                <div className="CartPage-image col-5">
                    <img width="fit-content" className="mr-2 img-fluid rounded shadow-sm" alt={this.props.data.name}
                        src={this.props.data.image} />
                </div>
                <div className="CartPage-price col-2">${this.props.data.price.toFixed(2)}</div>
                <div className="CartPage-quantity col-3">{this.props.data.quantity}</div>
                <div className="col-2"><a onClick={() => this.props.removeMe()} href="#" className="btn">🗑️</a></div>
            </div>
        )
    }
}

export default CartPageRow