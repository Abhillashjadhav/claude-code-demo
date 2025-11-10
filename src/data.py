"""Data loader for Read API 2.0 demo."""
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class DataStore:
    """In-memory data store for products and variant groups."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.products: List[Dict] = []
        self.groups: List[Dict] = []
        self._load_data()

    def _load_data(self):
        """Load products and groups from JSON files."""
        products_file = self.data_dir / "products.json"
        groups_file = self.data_dir / "groups.json"

        if products_file.exists():
            with open(products_file, 'r') as f:
                self.products = json.load(f)

        if groups_file.exists():
            with open(groups_file, 'r') as f:
                self.groups = json.load(f)

    def get_product(self, mplvid: str, market: Optional[str] = None) -> Optional[Dict]:
        """
        Get a single product by MPLVID.

        Args:
            mplvid: MarketplaceListingVariantID
            market: Optional market context filter

        Returns:
            Product dict if found, None otherwise
        """
        for product in self.products:
            if product.get("mplvid") == mplvid:
                # If market is specified, check if product is available in that market
                if market:
                    product_market = product.get("marketContext")
                    available_markets = product.get("availableMarkets", [])
                    if market != product_market and market not in available_markets:
                        continue
                return product
        return None

    def get_group(self, variant_group_id: str, market: Optional[str] = None) -> Optional[Dict]:
        """
        Get a variant group by variantGroupId.

        Args:
            variant_group_id: Variant group identifier
            market: Optional market context filter

        Returns:
            Group dict if found, None otherwise
        """
        for group in self.groups:
            if group.get("variantGroupId") == variant_group_id:
                # If market is specified, check market context
                if market and group.get("marketContext") != market:
                    continue
                return group
        return None

    def list_products(
        self,
        market: Optional[str] = None,
        class_id: Optional[str] = None,
        product_type: Optional[str] = None,
        has_barriers: Optional[bool] = None,
        last_updated_after: Optional[str] = None
    ) -> List[Dict]:
        """
        List products with optional filters.

        Args:
            market: Filter by market context
            class_id: Filter by class ID
            product_type: Filter by product type (SIMPLE, COMPOSITE, KIT)
            has_barriers: Filter by presence of barriers
            last_updated_after: Filter by lastUpdated timestamp (ISO 8601)

        Returns:
            List of matching products
        """
        results = []

        for product in self.products:
            # Market filter
            if market:
                product_market = product.get("marketContext")
                available_markets = product.get("availableMarkets", [])
                if market != product_market and market not in available_markets:
                    continue

            # Class ID filter
            if class_id and product.get("classId") != class_id:
                continue

            # Product type filter
            if product_type and product.get("productType") != product_type:
                continue

            # Barriers filter
            if has_barriers is not None:
                barrier_reasons = product.get("statusDetails", {}).get("barrierReasons", [])
                has_product_barriers = len(barrier_reasons) > 0
                if has_barriers != has_product_barriers:
                    continue

            # Last updated filter
            if last_updated_after:
                try:
                    cutoff_dt = datetime.fromisoformat(last_updated_after.replace('Z', '+00:00'))
                    product_dt = datetime.fromisoformat(product.get("lastUpdated", "").replace('Z', '+00:00'))
                    if product_dt <= cutoff_dt:
                        continue
                except (ValueError, AttributeError):
                    # Skip invalid dates
                    continue

            results.append(product)

        return results


# Global data store instance
_store = None


def get_store() -> DataStore:
    """Get or create the global data store instance."""
    global _store
    if _store is None:
        _store = DataStore()
    return _store
