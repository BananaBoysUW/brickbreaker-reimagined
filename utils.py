from Vector2D import Vector2D


def map_val(inMin, inMax, outMin, outMax, n):
    """maps n from [inMin, inMax] -> [outMin, outMax]"""
    n = max(min(n, inMax), inMin)
    return outMin + ((n - inMin) / (inMax - inMin)) * (outMax - outMin)


def ltrb_rect_to_point(rect):
    """converts a rectangle represented by top left and bottom right points into a list of vertices"""
    l, t, r, b = rect
    return ((l, t), (r, t), (r, b), (l, b))


def points_to_lines(points):
    """converts a list of points into a list of lines connecting adjacent point pairs"""
    return list(zip(points, points[1:] + points[:1]))


def collide_detect_polygon_circle(polygon_lines, circle_center, circle_radius):
    """if a collision occurs, returns a Vector2D for the axis of reflection, otherwise None"""
    for p1, p2 in polygon_lines:
        a = Vector2D(*p1)
        b = Vector2D(*p2)
        c = circle_center

        ab = b - a
        ac = c - a
        bc = c - b
        ba = a - b

        # edges
        if ac.angle_with_deg(ab) < 90 and bc.angle_with_deg(ba) < 90:
            perp = ac.perp(ab)
            if perp.norm() <= circle_radius:
                return perp

        # corners
        if ac.norm() <= circle_radius:
            return ac
        if bc.norm() <= circle_radius:
            return bc
