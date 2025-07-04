import random

def create_deck():
    """52枚のトランプ山札を作成"""
    suits = ['♠', '♣', '♦', '♥']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [v + s for s in suits for v in values]
    random.shuffle(deck)
    return deck

def card_value(card):
    """カードの点数を返す"""
    v = card[:-1]
    if v in ['J', 'Q', 'K']:
        return 10
    elif v == 'A':
        return 11
    else:
        return int(v)

def hand_value(hand):
    """手札の合計点を計算（Aは11または1）"""
    total = sum(card_value(card) for card in hand)
    ace_count = sum(1 for card in hand if card.startswith('A'))
    while total > 21 and ace_count:
        total -= 10
        ace_count -= 1
    return total

def print_hand(name, hand):
    """手札と合計点を表示"""
    print(f"{name}の手札: {', '.join(hand)} (合計: {hand_value(hand)})")

def blackjack_game():
    deck = create_deck()
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    print_hand("あなた", player)
    print(f"ディーラーの手札: {dealer[0]}, ??")

    # プレイヤーのターン
    while hand_value(player) < 21:
        action = input("ヒットしますか？ (h:ヒット / s:スタンド): ").lower()
        if action == 'h':
            card = deck.pop()
            print(f"あなたは {card} を引きました")
            player.append(card)
            print_hand("あなた", player)
        elif action == 's':
            break

    # プレイヤーがバーストした場合
    if hand_value(player) > 21:
        print("あなたはバーストしました！負けです。")
        return

    # ディーラーのターン
    print_hand("ディーラー", dealer)
    while hand_value(dealer) < 17:
        card = deck.pop()
        print(f"ディーラーは {card} を引きました")
        dealer.append(card)
        print_hand("ディーラー", dealer)

    # 勝敗判定
    player_score = hand_value(player)
    dealer_score = hand_value(dealer)

    if dealer_score > 21 or player_score > dealer_score:
        print("あなたの勝ち！")
    elif player_score == dealer_score:
        print("引き分け！")
    else:
        print("あなたの負け…")

if __name__ == "__main__":
    blackjack_game()
