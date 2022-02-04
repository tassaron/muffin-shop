/* This component gets the product information from the page HTML
 * and composes the Product Page out of other components.
*/
import React, { Component } from "react";
import ProductSlideshow from "./ProductSlideshow";
import ProductDescription from "./ProductDescription";


class ProductPage extends Component {
    constructor() {
        super();

        const getNodeOrError = function(name) {
            const node = document.getElementById(name);
            if (!node) {
                throw new ReferenceError(`Missing DOM node with ID ${name}`);
            }
            return node
        }

        // Ensure we're inside the ProductPage-row
        this.rowNode = getNodeOrError("ProductPage-row");

        // Get `productName`
        const nameNode = getNodeOrError("ProductPage-name");
        this.productName = nameNode.innerHTML;

        // Get `slideImages`
        const slidesNode = getNodeOrError("ProductPage-slides");
        this.slideImages = slidesNode.innerHTML.split(",");
        slidesNode.innerHTML = "";
    }

    render() {
        const productDescription = this.getProductDescription();

        return (
            <div className="row">
                <div className="col">
                    <ProductSlideshow slideImages={this.slideImages} productName={this.productName} />
                </div>
                { ( () => { if (productDescription) return <ProductDescription content={productDescription} /> } )() }
            </div>
        )
    }

    getProductDescription() {
        const productDescriptionNode = document.getElementById("ProductPage-description");
        if (!productDescriptionNode) {
            return "";
        }
        const productDescription = productDescriptionNode.innerHTML;
        this.rowNode.removeChild(productDescriptionNode);
        return productDescription;
    }
}

export default ProductPage