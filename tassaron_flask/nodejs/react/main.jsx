import React from "react";
import ReactDOM from "react-dom";
import ProductSlideshowFromHtml from "./ProductSlideshowFromHtml";
import ProductPageButtons from "./ProductPageButtons";
import getNodeOrError from "./util";
import "./styles.css";
 
function renderIfExists(comp, elemId) {
    const node = document.getElementById(elemId);
    if (node) {
        ReactDOM.render(comp, node);
    }
}

renderIfExists(<ProductSlideshowFromHtml />, "ProductPage-slideshow");

const node = document.getElementById("ProductPage-buttons");
if (node) {
    ReactDOM.render(
        <ProductPageButtons
            stock={Number(getNodeOrError("ProductPage-stock").innerHTML)}
            initialQuantity={Number(getNodeOrError("ProductPage-quantity").innerText)}
            downBtn={getNodeOrError("ProductPage-quantity-down").outerHTML}
            upBtn={getNodeOrError("ProductPage-quantity-up").outerHTML}
            />,
        node
    );
}