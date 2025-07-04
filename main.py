import random

# ========================
# プレイヤークラスの定義
# ========================
class Player:
    def __init__(self, name, money=1000):
        self.name = name
        self.money = money
        self.hand = []
        self.bet = 0
        self.win = 0
        self.lose = 0
        self.draw = 0

    def reset_hand(self):
        """手札とベット額をリセット"""
        self.hand = []
        self.bet = 0

    def record_result(self, result):
        """勝敗記録を更新"""
        if result == "win":
            self.win += 1
        elif result == "lose":
            self.lose += 1
        elif result == "draw":
            self.draw += 1

# ========================
# ゲーム用関数
# ========================
def create_deck():
    """シャッフル済みの52枚の山札を作成"""
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
    return int(v)

def hand_value(hand):
    """手札の合計点数を計算（Aは11 or 1）"""
    total = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c.startswith('A'))
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def print_hand(name, hand):
    """手札を表示"""
    print(f"{name}の手札: {', '.join(hand)}（合計: {hand_value(hand)}）")

def place_bet(player):
    """プレイヤーにベットさせる"""
    while True:
        try:
            print(f"{player.name}の所持金: {player.money}")
            bet = int(input(f"{player.name}のベット額を入力してください: "))
            if 0 < bet <= player.money:
                player.bet = bet
                player.money -= bet
                break
            else:
                print("無効なベット額です。")
        except ValueError:
            print("数値で入力してください。")

def player_turn(player, deck):
    """プレイヤーのターン（ヒット／スタンド）"""
    while hand_value(player.hand) < 21:
        print_hand(player.name, player.hand)
        action = input(f"{player.name}のターン。ヒット(h) or スタンド(s): ").lower()
        if action == 'h':
            card = deck.pop()
            print(f"{player.name}は {card} を引きました")
            player.hand.append(card)
        elif action == 's':
            break

def dealer_turn(dealer, deck):
    """ディーラーのターン（17未満ならヒット）"""
    print_hand("ディーラー", dealer.hand)
    while hand_value(dealer.hand) < 17:
        card = deck.pop()
        print(f"ディーラーは {card} を引きました")
        dealer.hand.append(card)
        print_hand("ディーラー", dealer.hand)

def settle_bet(player, dealer_score):
    """勝敗判定と所持金の更新"""
    player_score = hand_value(player.hand)
    print_hand(player.name, player.hand)

    if player_score > 21:
        print(f"{player.name}はバーストしました。負け。")
        player.record_result("lose")
    elif dealer_score > 21 or player_score > dealer_score:
        print(f"{player.name}の勝ち！ +{player.bet * 2}")
        player.money += player.bet * 2
        player.record_result("win")
    elif player_score == dealer_score:
        print(f"{player.name}は引き分け。ベット返還")
        player.money += player.bet
        player.record_result("draw")
    else:
        print(f"{player.name}の負け。")
        player.record_result("lose")

def show_stats(players):
    """各プレイヤーの勝敗記録を表示"""
    print("\n=== 勝敗記録 ===")
    for p in players:
        print(f"{p.name}: 勝ち:{p.win} / 負け:{p.lose} / 引き分け:{p.draw} / 所持金:{p.money}")

# ========================
# ゲームメイン処理
# ========================
def blackjack_game():
    players = [Player("プレイヤー1"), Player("プレイヤー2")]
    dealer = Player("ディーラー")

    while True:
        deck = create_deck()
        dealer.reset_hand()
        dealer.hand = [deck.pop(), deck.pop()]

        for p in players:
            p.reset_hand()
            place_bet(p)
            p.hand = [deck.pop(), deck.pop()]

        for p in players:
            player_turn(p, deck)

        dealer_turn(dealer, deck)
        dealer_score = hand_value(dealer.hand)

        for p in players:
            settle_bet(p, dealer_score)

        show_stats(players)

        again = input("\n次のラウンドをプレイしますか？ (y/n): ").lower()
        if again != 'y':
            print("ゲーム終了。お疲れ様でした！")
            break

if __name__ == "__main__":
    blackjack_game()
