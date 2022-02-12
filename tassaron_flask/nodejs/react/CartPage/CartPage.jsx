import React, { Component } from "react";
import CartPageColumn from "./CartPageColumn";
import CartPageRow from "./CartPageRow";
import { getNodeOrError } from "../util";


class CartPage extends Component {
    constructor() {
        super();
        const containerNode = getNodeOrError("CartPage-container");
        const rowNodes = document.getElementsByClassName("CartPage-row");
        const rowData = [];
        for (let node of rowNodes) {
            rowData.push({
                id: node.dataset.productId,
                name: node.getElementsByClassName("CartPage-name")[0].innerText,
                image: node.getElementsByClassName("CartPage-image")[0].children[0].getAttribute("src"),
                price: Number(node.getElementsByClassName("CartPage-price")[0].innerText.slice(1)),
                quantity: Number(node.getElementsByClassName("CartPage-quantity")[0].innerText)
            });
            containerNode.removeChild(node);
        }
        this.state = {
            rows: rowData
        }
    }

    render() {
        return (
            <CartPageColumn>
                {
                    this.state.rows.map(
                        (row) => {
                            return <CartPageRow data={row} />
                        }
                    )
                }
            </CartPageColumn>
        )
    }
}

export default CartPage