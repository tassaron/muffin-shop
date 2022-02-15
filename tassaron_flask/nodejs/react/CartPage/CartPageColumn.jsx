import { Component } from "react";

class CartPageColumn extends Component {
    render() {
        return (
            <>
                {this.props.children}
                {this.props.totalPrice > 0 ? (
                    <div className="row mt-2 border-top">
                        <div className="col-md-5 col-3 d-flex justify-content-end text-decoration-underline">
                            total price
                        </div>
                        <div className="col-2 text-center">
                            ${this.props.totalPrice.toFixed(2)}
                        </div>
                    </div>
                ) : (
                    <></>
                )}
            </>
        );
    }
}

export default CartPageColumn;
