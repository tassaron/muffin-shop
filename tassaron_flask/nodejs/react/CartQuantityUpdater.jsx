import { Component } from "react";

class CartQuantityUpdater extends Component {
    constructor(props) {
        super(props);
        this.state = {
            quantity: this.props.initialQuantity
        }
    }

    componentDidMount() {
        this.btnNode = document.querySelector(`.ProductPage-cart-btn-${this.props.productId}[data-product-id='${this.props.productId}']`);
        this.watchedNode = document.querySelector(`.product-description[data-product-id='${this.props.productId}']`);
        this.timer = setInterval(
            () => this.tick(),
            5000
        );
    }
    componentWillUnmount() {
        clearInterval(this.timer);
    }

    tick() {
        if (this.watchedNode.childElementCount == 2) {
            return
        }
        const child = this.watchedNode.children[2];
        const message = child.innerText;
        const newValue = Number(message.split(" ")[1]);
        console.log(newValue);
        this.watchedNode.removeChild(child);
        this.setState((state, props) => ({
            quantity: state.quantity + newValue
        }));
        this.btnNode.classList.remove("btn-disabled");
    }

    render() {
        return (
            <div
                style={{ visibility: this.state.quantity > 0 ? "visible" : "hidden" }}
                className="product-buttons-cart-indicator-text text-center">
                <strong>
                    {this.state.quantity}
                </strong> in your cart
            </div>
        )
    }
}

export default CartQuantityUpdater