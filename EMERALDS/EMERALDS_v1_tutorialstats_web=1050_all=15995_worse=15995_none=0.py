from datamodel import OrderDepth, TradingState, Order, ConversionObservation, Product
from typing import List
import jsonpickle
import math

class Trader:
    def emerald_orders(self, order_depth: OrderDepth, fair_value: int, width: int, position: int, position_limit: int) -> List[Order]:
        orders: List[Order] = []

        sell_above_fv = [price for price in order_depth.sell_orders.keys() if price > fair_value + 1]
        baaf = min(sell_above_fv) if sell_above_fv else fair_value + 2

        buy_below_fv = [price for price in order_depth.buy_orders.keys() if price < fair_value - 1]
        bbbf = max(buy_below_fv) if buy_below_fv else fair_value - 2

        if len(order_depth.sell_orders) != 0:
            best_ask = min(order_depth.sell_orders.keys())
            best_ask_amount = -1 * order_depth.sell_orders[best_ask]
            if best_ask < fair_value:
                quantity = min(best_ask_amount, position_limit - position)
                if quantity > 0:
                    orders.append(Order("EMERALDS", int(best_ask), quantity))

        if len(order_depth.buy_orders) != 0:
            best_bid = max(order_depth.buy_orders.keys())
            best_bid_amount = order_depth.buy_orders[best_bid]
            if best_bid > fair_value:
                quantity = min(best_bid_amount, position_limit + position)
                if quantity > 0:
                    orders.append(Order("EMERALDS", int(best_bid), -quantity))

        buy_order_volume, sell_order_volume = self.clear_position_order(
            orders, order_depth, position, position_limit, "EMERALDS",
            sum([o.quantity for o in orders if o.quantity > 0]),
            sum([-o.quantity for o in orders if o.quantity < 0]),
            fair_value, width
        )

        buy_quantity = position_limit - (position + buy_order_volume)
        if buy_quantity > 0:
            orders.append(Order("EMERALDS", int(bbbf + 1), buy_quantity))

        sell_quantity = position_limit + (position - sell_order_volume)
        if sell_quantity > 0:
            orders.append(Order("EMERALDS", int(baaf - 1), -sell_quantity))

        return orders

    def clear_position_order(self, orders: List[Order], order_depth: OrderDepth, position: int, position_limit: int, product: str,
                             buy_order_volume: int, sell_order_volume: int, fair_value: float, width: int):

        position_after_take = position + buy_order_volume - sell_order_volume
        fair_for_bid = math.floor(fair_value)
        fair_for_ask = math.ceil(fair_value)

        buy_quantity = position_limit - (position + buy_order_volume)
        sell_quantity = position_limit + (position - sell_order_volume)

        if position_after_take > 0 and fair_for_ask in order_depth.buy_orders:
            clear_quantity = min(order_depth.buy_orders[fair_for_ask], position_after_take)
            sent_quantity = min(sell_quantity, clear_quantity)
            orders.append(Order(product, int(fair_for_ask), -abs(sent_quantity)))
            sell_order_volume += abs(sent_quantity)

        if position_after_take < 0 and fair_for_bid in order_depth.sell_orders:
            clear_quantity = min(abs(order_depth.sell_orders[fair_for_bid]), abs(position_after_take))
            sent_quantity = min(buy_quantity, clear_quantity)
            orders.append(Order(product, int(fair_for_bid), abs(sent_quantity)))
            buy_order_volume += abs(sent_quantity)

        return buy_order_volume, sell_order_volume

    def run(self, state: TradingState):
        result = {}

        fair_value = 10000
        width = 2
        position_limit = 50

        if "EMERALDS" in state.order_depths:
            position = state.position.get("EMERALDS", 0)
            orders = self.emerald_orders(
                state.order_depths["EMERALDS"],
                fair_value,
                width,
                position,
                position_limit
            )
            result["EMERALDS"] = orders

        traderData = jsonpickle.encode({})
        conversions = 0

        return result, conversions, traderData