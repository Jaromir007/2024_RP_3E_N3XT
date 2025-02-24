class MonotoneChain:
    def __init__(self):
        pass

    def _remove_duplicates(self, points):
        unique = []
        seen = set()
        for p in points:
            if tuple(p) not in seen:
                seen.add(tuple(p))
                unique.append(p)
        return unique

    def _cross_product(self, p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

    def _convex_hull(self, points):
        points.sort()
        lower = []
        for p in points:
            while len(lower) >= 2 and self._cross_product(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and self._cross_product(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        return lower[:-1] + upper[:-1]

    def get_outline(self, points):
        unique_points = self._remove_duplicates(points)
        return self._convex_hull(unique_points)